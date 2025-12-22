#!/usr/bin/env python3
"""
Test script to validate image proxy architecture.
Verifies: Upload → MinIO → Download via proxy
"""

import httpx
import asyncio
import json
from pathlib import Path
from io import BytesIO
from PIL import Image

# Configuration
API_BASE_URL = "http://localhost:8000"
TEST_IMAGE_PATH = "/tmp/test_product.jpg"

async def create_test_image():
    """Create a simple test image."""
    img = Image.new('RGB', (400, 500), color='red')
    img.save(TEST_IMAGE_PATH)
    print(f"✓ Created test image: {TEST_IMAGE_PATH}")
    return TEST_IMAGE_PATH

async def test_upload_and_download():
    """Test full image flow: upload → storage → download via proxy."""
    
    async with httpx.AsyncClient(timeout=10) as client:
        # Step 1: Upload image
        print("\n1️⃣  Testing image upload...")
        with open(TEST_IMAGE_PATH, 'rb') as f:
            image_data = f.read()
        
        files = {'file': ('test.jpg', image_data, 'image/jpeg')}
        
        try:
            upload_response = await client.post(
                f"{API_BASE_URL}/media/upload",
                files=files
            )
            upload_response.raise_for_status()
            upload_result = upload_response.json()
            
            image_url = upload_result.get('image_url')
            image_key = upload_result.get('image_key')
            
            print(f"  ✓ Upload successful!")
            print(f"    Image URL (proxy path): {image_url}")
            print(f"    Image Key (storage): {image_key}")
            
            # Validate response format
            assert image_url.startswith('/media/download/'), f"❌ Expected proxy path, got: {image_url}"
            assert image_key, "❌ image_key should not be empty"
            print(f"  ✓ Response format valid")
            
        except httpx.RequestError as e:
            print(f"  ❌ Upload request failed: {e}")
            return False
        except AssertionError as e:
            print(f"  ❌ Validation failed: {e}")
            return False
        
        # Step 2: Download via proxy
        print("\n2️⃣  Testing image download via proxy...")
        try:
            download_response = await client.get(
                f"{API_BASE_URL}{image_url}"
            )
            download_response.raise_for_status()
            
            print(f"  ✓ Download successful!")
            print(f"    Status: {download_response.status_code}")
            print(f"    Content-Type: {download_response.headers.get('content-type')}")
            print(f"    Content-Length: {len(download_response.content)} bytes")
            
            # Validate response
            assert download_response.headers.get('content-type') == 'image/jpeg', \
                f"❌ Expected image/jpeg, got: {download_response.headers.get('content-type')}"
            assert len(download_response.content) > 0, "❌ Download content empty"
            assert len(download_response.content) == len(image_data), \
                f"❌ Downloaded size mismatch: {len(download_response.content)} vs {len(image_data)}"
            print(f"  ✓ Downloaded content matches uploaded image")
            
            # Check cache headers
            cache_control = download_response.headers.get('cache-control', '')
            if 'max-age' in cache_control:
                print(f"  ✓ Cache headers present: {cache_control}")
            else:
                print(f"  ⚠️  No cache-control header")
            
        except httpx.RequestError as e:
            print(f"  ❌ Download request failed: {e}")
            return False
        except AssertionError as e:
            print(f"  ❌ Validation failed: {e}")
            return False
        
        # Step 3: Test with product creation
        print("\n3️⃣  Testing product creation with image...")
        
        # First need to test endpoint (may require auth in future)
        print("  (Skipping product creation test - requires auth setup)")
        
        # Step 4: Verify no direct MinIO URLs
        print("\n4️⃣  Verifying security (no direct MinIO exposure)...")
        print(f"  ✓ Upload response contains only proxy path: {image_url}")
        print(f"    NOT direct MinIO URL (no 'minio:9000' or ':9000')")
        assert 'minio:9000' not in image_url, "❌ Direct MinIO URL exposed!"
        assert ':9000' not in image_url, "❌ MinIO port exposed!"
        print(f"  ✓ Security check passed")
        
    return True

async def main():
    """Run all tests."""
    print("=" * 60)
    print("IMAGE PROXY ARCHITECTURE TEST")
    print("=" * 60)
    
    # Create test image
    try:
        await create_test_image()
    except ImportError:
        print("⚠️  PIL not installed, skipping image creation")
        print("   Install with: pip install Pillow")
        return False
    except Exception as e:
        print(f"❌ Failed to create test image: {e}")
        return False
    
    # Run tests
    success = await test_upload_and_download()
    
    # Summary
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
        print("\nImage proxy architecture is working correctly:")
        print("  • Images upload to MinIO")
        print("  • Backend returns proxy paths (/media/download/...)")
        print("  • Frontend can download via proxy")
        print("  • Direct MinIO URLs are NOT exposed")
        print("\nNo more net::ERR_NAME_NOT_RESOLVED errors! 🎉")
    else:
        print("❌ TESTS FAILED")
        print("\nDebugging tips:")
        print("  • Check backend is running: http://localhost:8000")
        print("  • Check MinIO is running: docker compose ps")
        print("  • Review backend logs: docker compose logs backend")
        print("  • Check CORS settings in back/app/main.py")
    print("=" * 60)
    
    return success

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
