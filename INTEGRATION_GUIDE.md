# Yoga Pose Detector - Integration Guide

## Summary
Completely rebuilt the integration between frontend React app and backend Python WebSocket server to support both single asana practice and full routine sequences with proper session management and audio feedback.

## Major Changes

### 1. Backend Improvements (main.py)

**Session Management:**
- Added proper session initialization with mode detection (single vs routine)
- Each client session now maintains:
  - Mode (single asana or full routine)
  - Asana sequence (varies based on mode)
  - Current position in sequence
  - Hold timer and feedback cooldown
- Sessions are isolated per WebSocket connection

**Asana ID Mapping:**
- Created mapping from frontend asana IDs to backend pose names:
  - 1: pranamasana
  - 2: hastauttanasana
  - 3: hastapadasana
  - 4: right_ashwa_sanchalanasana
  - 5: dandasana
  - 6: ashtanga_namaskara
  - 7: bhujangasana
  - 8: adho_mukha_svanasana
  - 9: left_ashwa_sanchalanasana

**Dual Mode Operation:**
- **Single Mode**: Practices one asana, exits after holding correctly for 3 seconds
- **Routine Mode**: Progresses through sequence automatically after each pose

**Audio Feedback:**
- TTS audio generated server-side and sent as base64 MP3
- Audio feedback includes:
  - Initial pose announcement
  - Pose completion messages
  - Next pose transitions
  - Joint adjustment instructions (limited to 2 joints)
  - Routine completion message

**Message Protocol:**
- Init message: `{type: "init", mode: "single"|"routine", asanaIds: [1,2,3], routineName: "..."}`
- Frame message: `{imageData: "base64..."}`
- Response: `{data: 0-5, confidence: 0-1, pose_name: "...", audio_data: "base64..."}`

**Response Codes:**
- 0: No pose detected
- 1: Incorrect pose
- 2: Correct pose (holding)
- 3: Partial (needs adjustments)
- 4: Moving to next pose
- 5: Practice complete

### 2. Frontend Improvements

**CameraView.tsx:**
- Sends initialization message on connection with mode and asana list
- Waits for session initialization before sending frames
- Displays current pose name in header
- Shows completion alert and auto-exits after 2 seconds
- Properly handles both single and routine modes

**useWebSocket.ts:**
- Added `sendInit()` function for session initialization
- Implemented audio playback using HTML5 Audio API
- Decodes base64 MP3 audio from backend
- Handles init response messages
- Improved error handling for malformed messages

**Context (AppContext.tsx):**
- Already had proper state management for:
  - Selected routine
  - Selected asana (for single practice)
  - Full routine flag

### 3. Backend Fixes (pose_equal_check.py)

**Accuracy Calculation:**
- Changed accuracy return from percentage (0-100) to decimal (0-1)
- Now returns values like 0.85 instead of 85.0
- Frontend multiplies by 100 for display

**Error Handling:**
- Added safety checks for empty landmarks
- Returns sensible defaults on errors
- Logs missing ideal pose images

### 4. Asset Management

**Created Missing Pose Image:**
- Copied `left_ashwa_sanchalanasana.jpg` as `right_ashwa_sanchalanasana.jpg`
- Both use the same reference image (acceptable for initial version)

## How It Works Now

### Complete Flow:

1. **User Selection:**
   - User picks routine (Surya Namaskar) or individual asana
   - Frontend stores selection in context

2. **Camera Initialization:**
   - CameraView component opens camera
   - Waits for WebSocket connection

3. **Session Setup:**
   - Frontend sends init message with mode and asana IDs
   - Backend creates session state
   - Backend sends welcome audio and pose name
   - Frontend enables frame capture

4. **Practice Loop:**
   - Every 2 seconds: frontend captures and sends frame
   - Backend processes pose detection
   - Backend sends response with status, accuracy, audio
   - Frontend displays status and plays audio

5. **Pose Progression (Routine Mode):**
   - User holds correct pose for 3 seconds
   - Backend advances to next pose
   - Sends transition audio and new pose name
   - Frontend updates display
   - Repeats until sequence complete

6. **Completion:**
   - Backend sends status code 5
   - Frontend shows completion alert
   - Auto-exits to routine detail page after 2 seconds

### Key Features:

- **Real-time feedback**: Visual status bars with color coding
- **Audio guidance**: Spoken instructions for adjustments
- **Progress tracking**: Automatic advancement through sequences
- **Flexible modes**: Single pose practice or full routines
- **Smart cooldown**: Limits audio feedback to every 5 seconds
- **Hold detection**: Requires 3-second hold on correct pose

## Testing

- Frontend builds successfully without TypeScript errors
- Backend has proper error handling
- WebSocket protocol is well-defined
- Audio playback tested in browser
- Session management handles multiple clients

## How to Run

### Quick Start (Using Scripts):

**Terminal 1 - Backend:**
```bash
./start_backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start_frontend.sh
```

### Manual Start:

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

The backend runs at `ws://localhost:8765` (note: uses 0.0.0.0 for WSL compatibility)
The frontend runs at `http://localhost:5173`

### Usage:

1. Open browser to frontend URL
2. Allow camera permissions
3. Click "Surya Namaskar" routine card
4. Choose:
   - "Start Full Routine" for complete sequence
   - Individual pose card for single practice
5. Follow audio and visual guidance
6. Hold poses correctly for 3 seconds to progress

## Architecture Benefits

- **Stateful sessions**: Each user has isolated practice session
- **Mode-aware**: Backend adapts behavior based on single/routine mode
- **Scalable**: Can add new routines and poses easily
- **Maintainable**: Clear separation of concerns
- **Extensible**: Easy to add features like:
  - Custom hold times
  - Different difficulty levels
  - Progress tracking/history
  - Multiple routine support

## Troubleshooting

### Camera not working:
- Ensure browser has camera permissions
- Check if another app is using the camera
- Try the camera toggle button

### WebSocket connection fails:
- Verify backend is running on port 8765
- Check firewall settings
- Ensure no other service is using the port

### Audio not playing:
- Check browser audio permissions
- Unmute the tab if muted
- Some browsers require user interaction before audio plays

### Pose not detected:
- Ensure good lighting
- Stand 6-8 feet from camera
- Wear contrasting clothing
- Full body should be visible in frame
