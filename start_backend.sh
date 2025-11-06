#!/bin/bash

echo "Starting Yoga Pose Detector Backend..."
echo "======================================="
echo ""

cd backend

if ! command -v python3 &> /dev/null; then
    echo "Error: python3 not found. Please install Python 3."
    exit 1
fi

echo "Checking dependencies..."
python3 -c "import cv2, mediapipe, websockets, pygame, gtts" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing required dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Starting WebSocket server on ws://localhost:8765..."
echo "Press Ctrl+C to stop"
echo ""

python3 main.py
