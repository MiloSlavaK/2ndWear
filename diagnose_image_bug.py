#!/usr/bin/env python3
"""
Diagnostic script for image loading bug.
Tests the entire flow: upload -> storage -> download -> browser rendering.
"""

import httpx
import asyncio
import io
from PIL import Image
import sys

API_BASE_URL = "http://localhost:8000"

async def test_image_flow():
    """Test complete image flow with detailed diagnostics."""
    
    print("=" * 70)
    print("IMAGE LOADING BUG DIAGNOSTIC")
    print("=" * 70)
    
    # Create test image
    print("\n1️⃣  Creating test image...")
    img = Image.new('RGB', (200, 300), color='blue')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    test_image_data = img_bytes.getvalue()
    print(f"   ✓ Test image created: {len(test_image_data)} bytes")
    
    async with httpx.AsyncClient(timeout=10) as client:
        # Step 1: Upload image
        print("\n2️⃣  Testing image upload...")
        try:
            upload_response = await client.post(
                f"{API_BASE_URL}/media/upload",
                files={"file": ("test.jpg", test_image_data, "image/jpeg")}
            )
            upload_response.raise_for_status()
            upload_data = upload_response.json()
            image_url = upload_data.get("image_url")
            image_key = upload_data.get("image_key")
            
            print(f"   ✓ Upload successful!")
            print(f"     Image URL: {image_url}")
            print(f"     Image Key: {image_key}")
            
            if not image_url or not image_key:
                print(f"   ❌ Invalid response: {upload_data}")
                return False
                
        except Exception as e:
            print(f"   ❌ Upload failed: {e}")
            return False
        
        # Step 2: Download image
        print("\n3️⃣  Testing image download via proxy...")
        try:
            download_response = await client.get(
                f"{API_BASE_URL}{image_url}"
            )
            download_response.raise_for_status()
            
            print(f"   ✓ Download successful!")
            print(f"     Status Code: {download_response.status_code}")
            print(f"     Content-Type: {download_response.headers.get('content-type')}")
            print(f"     Content-Length: {download_response.headers.get('content-length')}")
            print(f"     Actual Size: {len(download_response.content)} bytes")
            print(f"     Cache-Control: {download_response.headers.get('cache-control')}")
            
            # Verify content
            if not download_response.content:
                print(f"   ❌ ERROR: Response body is EMPTY!")
                return False
            
            if len(download_response.content) != len(test_image_data):
                print(f"   ⚠️  WARNING: Size mismatch!")
                print(f"     Expected: {len(test_image_data)} bytes")
                print(f"     Received: {len(download_response.content)} bytes")
            else:
                print(f"   ✓ Content size matches uploaded image")
            
            # Try to open as image
            try:
                test_img = Image.open(io.BytesIO(download_response.content))
                print(f"   ✓ Downloaded content is valid image: {test_img.format} {test_img.size}")
            except Exception as e:
                print(f"   ❌ ERROR: Downloaded content is NOT a valid image: {e}")
                return False
                
        except Exception as e:
            print(f"   ❌ Download failed: {e}")
            return False
        
        # Step 3: Check headers for browser compatibility
        print("\n4️⃣  Checking response headers for browser compatibility...")
        required_headers = {
            "content-type": "image/jpeg",
            "content-length": str(len(test_image_data)),
            "cache-control": None  # Just needs to exist
        }
        
        issues = []
        for header, expected in required_headers.items():
            actual = download_response.headers.get(header)
            if not actual:
                issues.append(f"   ❌ Missing header: {header}")
            elif expected and actual != expected:
                issues.append(f"   ⚠️  Header mismatch for {header}: expected {expected}, got {actual}")
            else:
                print(f"   ✓ {header}: {actual}")
        
        if issues:
            for issue in issues:
                print(issue)
        
        # Step 4: Check CORS headers
        print("\n5️⃣  Checking CORS headers...")
        cors_headers = {
            "access-control-allow-origin": None,
            "access-control-expose-headers": None,
        }
        
        for header in cors_headers:
            value = download_response.headers.get(header)
            if value:
                print(f"   ✓ {header}: {value}")
            else:
                print(f"   ⚠️  Missing CORS header: {header}")
        
        # Step 5: Simulate browser fetch
        print("\n6️⃣  Simulating browser fetch with CORS...")
        try:
            browser_response = await client.get(
                f"{API_BASE_URL}{image_url}",
                headers={"Origin": "http://localhost:5173"}
            )
            
            if "access-control-allow-origin" not in browser_response.headers:
                print(f"   ⚠️  CORS not properly configured for cross-origin requests")
            else:
                print(f"   ✓ CORS properly configured")
                print(f"     Allow-Origin: {browser_response.headers.get('access-control-allow-origin')}")
            
        except Exception as e:
            print(f"   ❌ CORS test failed: {e}")
    
    print("\n" + "=" * 70)
    print("DIAGNOSTIC COMPLETE")
    print("=" * 70)
    
    return True

async def main():
    try:
        success = await test_image_flow()
        if success:
            print("\n✅ Image flow is working correctly!")
            print("\nIf images still don't display in browser:")
            print("  1. Check browser console for errors (F12)")
            print("  2. Check Network tab - verify response has content")
            print("  3. Check Content-Type and Content-Length headers")
            print("  4. Try hard refresh (Ctrl+Shift+R or Cmd+Shift+R)")
            return 0
        else:
            print("\n❌ Image flow has issues - see above")
            return 1
    except KeyboardInterrupt:
        print("\n\nDiagnostic interrupted")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
