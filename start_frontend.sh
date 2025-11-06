#!/bin/bash

echo "Starting Yoga Pose Detector Frontend..."
echo "========================================"
echo ""

cd frontendreact

if ! command -v npm &> /dev/null; then
    echo "Error: npm not found. Please install Node.js and npm."
    exit 1
fi

if [ ! -d "node_modules" ]; then
    echo "Installing dependencies..."
    npm install
fi

echo ""
echo "Starting development server..."
echo "The app will open in your browser automatically"
echo "Press Ctrl+C to stop"
echo ""

npm run dev
