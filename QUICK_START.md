# Yoga Pose Detector - Quick Start

## What Was Fixed

The yoga pose detector now properly works as a complete application where:
- Users can practice individual poses OR complete routines
- The frontend sends camera frames to the backend
- The backend analyzes poses and provides real-time audio + visual feedback
- Automatic progression through poses when held correctly for 3 seconds
- Sessions are properly managed with distinct modes (single/routine)

## Starting the Application

### Option 1: Using Scripts (Recommended)

**Terminal 1:**
```bash
./start_backend.sh
```

**Terminal 2:**
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

## Using the Application

1. Open browser to `http://localhost:5173`
2. Allow camera permissions when prompted
3. Click "Surya Namaskar" card on home page
4. Choose your practice mode:
   - **"Start Full Routine"** - Complete 12-pose sequence with auto-progression
   - **Click individual pose card** - Practice single pose

### During Practice:

- **Green status** = Perfect pose, hold it
- **Amber status** = Almost there, listen to adjustment instructions
- **Red status** = Incorrect, adjust your position
- **Blue status** = Moving to next pose

### Audio Feedback:

- Announces current pose
- Gives specific joint adjustment instructions
- Confirms when pose is complete
- Announces next pose in sequence

### Tips:

- Stand 6-8 feet from camera
- Ensure full body is visible
- Good lighting helps
- Wear contrasting clothing
- Hold correct poses for 3 seconds to progress

## Architecture Overview

### Backend (Python WebSocket Server)
- Receives camera frames from frontend
- Uses MediaPipe for pose detection
- Compares with ideal poses
- Generates audio feedback (gTTS)
- Manages session state per client
- Sends real-time responses

### Frontend (React + TypeScript)
- Captures camera frames every 2 seconds
- Sends frames to backend via WebSocket
- Displays pose name and feedback
- Plays audio instructions
- Handles routine progression
- Beautiful UI with Tailwind CSS

### Communication Protocol

**Init Message (Frontend → Backend):**
```json
{
  "type": "init",
  "mode": "single" | "routine",
  "asanaIds": [1, 2, 3, ...],
  "routineName": "Surya Namaskar"
}
```

**Frame Message (Frontend → Backend):**
```json
{
  "imageData": "data:image/jpeg;base64,..."
}
```

**Response (Backend → Frontend):**
```json
{
  "data": 0-5,
  "confidence": 0.0-1.0,
  "pose_name": "pranamasana",
  "audio_data": "base64_encoded_mp3"
}
```

### Response Codes:
- `0` - No pose detected
- `1` - Incorrect pose
- `2` - Correct pose (holding)
- `3` - Partial (needs adjustments)
- `4` - Next pose
- `5` - Complete

## Project Structure

```
├── backend/
│   ├── main.py                    # WebSocket server
│   ├── PoseModule.py              # Pose detection
│   ├── pose_equal_check.py        # Pose comparison
│   ├── ideal_poses/               # Reference images
│   └── requirements.txt           # Python dependencies
│
├── frontendreact/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.tsx       # Routine selection
│   │   │   ├── RoutineDetailPage.tsx
│   │   │   └── CameraView.tsx     # Practice interface
│   │   ├── hooks/
│   │   │   ├── useCamera.ts       # Camera management
│   │   │   └── useWebSocket.ts    # Backend communication
│   │   ├── contexts/
│   │   │   └── AppContext.tsx     # State management
│   │   └── data/
│   │       └── routines.ts        # Routine definitions
│   └── package.json
│
├── start_backend.sh               # Backend launcher
├── start_frontend.sh              # Frontend launcher
└── INTEGRATION_GUIDE.md           # Detailed documentation
```

## Key Improvements Made

1. **Session Management**: Backend now maintains state per client
2. **Mode Support**: Single asana vs full routine differentiation
3. **Audio Feedback**: Real-time spoken instructions
4. **Proper Initialization**: Handshake protocol before practice
5. **Accuracy Display**: Normalized values (0-1) for consistency
6. **Auto-progression**: Smooth transitions between poses
7. **Error Handling**: Graceful degradation on failures
8. **TypeScript**: Type-safe frontend code

## Troubleshooting

**Camera not working:**
- Check browser permissions
- Try toggling camera using button
- Ensure no other app is using camera

**WebSocket fails:**
- Verify backend is running on port 8765
- Check firewall settings

**Audio not playing:**
- Check browser audio permissions
- Unmute tab if needed
- Some browsers block autoplay

**Pose not detected:**
- Improve lighting
- Stand further from camera
- Show full body in frame

## Next Steps

To enhance the application, consider:
- Add user accounts and progress tracking
- Support multiple routines
- Implement difficulty levels
- Add pose history and statistics
- Create mobile app version
- Add multiplayer/social features
