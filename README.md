# Yoga Pose Detector

AI-powered yoga assistant that provides real-time feedback on your yoga poses.

## Quick Start

### Option 1: Using Start Scripts (Recommended)

**Terminal 1 - Start Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
./start_frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
pip install -r requirements.txt
python3 main.py
```

**Terminal 2 - Frontend:**
```bash
cd frontendreact
npm install
npm run dev
```

The WebSocket server will run at `ws://localhost:8765`
The frontend will be available at `http://localhost:5173`

## How It Works

1. Choose a yoga routine (like Surya Namaskar) or practice individual poses
2. Allow camera access when prompted
3. The app captures frames from your camera and sends them to the backend
4. The backend analyzes your pose using MediaPipe and provides:
   - Visual feedback on screen
   - Audio feedback through text-to-speech
   - Accuracy percentage
   - Specific corrections for wrong joint angles

### Full Routine Mode

- Practice complete sequences like Surya Namaskar
- Hold each pose correctly for 3 seconds to progress automatically
- Track your progress through the routine
- Complete audio guidance throughout

### Single Pose Mode

- Practice individual poses at your own pace
- Get detailed feedback on your form
- Improve specific poses

## Backend API

The backend expects WebSocket messages with:

```json
{
  "asanaNumber": 1,
  "imageData": "base64_encoded_image"
}
```

And responds with:

```json
{
  "data": 2,
  "confidence": 0.95
}
```

Where `data` values mean:
- 0: No pose detected
- 1: Incorrect pose
- 2: Perfect pose
- 3: Partial/needs adjustment
