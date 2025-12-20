// src/firebase.js - ИСПРАВЛЕННАЯ версия
import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore"; // ← ДОБАВЬТЕ ЭТО

// Your web app's Firebase configuration
const firebaseConfig = {
    apiKey: "AIzaSyCMqA_PX2a8f4IMSBx1KwZUTDjUnVWndDk",
    authDomain: "ndwear-44349.firebasestorage.app",
    projectId: "ndwear-44349",
    storageBucket: "ndwear-44349.firebasestorage.app",
    messagingSenderId: "542192848266",
    appId: "1:542192848266:web:0f5c3d47bf44bc2c8a8c73",
    measurementId: "G-BVR6WGBN81"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Initialize Firestore (база данных) ← ДОБАВЬТЕ ЭТО
export const db = getFirestore(app); // ← ЭТО САМОЕ ВАЖНОЕ!

console.log("✅ Firebase Firestore подключен!");