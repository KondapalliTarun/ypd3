import asyncio
import websockets
import cv2 as cv
import PoseModule as pm
import pose_equal_check as pec
import json
import base64
import numpy as np
# Removed pygame import (no longer needed for server-side playback)
import gtts as gTTS
import io
import threading
import time

# Initialize pose detection modules
detector = pm.PoseDetector()
pose_similarity = pec.PoseSimilarity()
# Removed pygame.mixer.init() - Audio will be handled by the client

# Asana sequence
surya_namaskar_sequence = [
    "pranamasana",
    "hastauttanasana",
    "hastapadasana",
    "right_ashwa_sanchalanasana",
    "dandasana",
    "ashtanga_namaskara",
    "bhujangasana",
    "adho_mukha_svanasana",
    "left_ashwa_sanchalanasana",
    "hastapadasana",
    "hastauttanasana",
    "pranamasana"
]

# Dictionary to store the state of each client
client_states = {}

# --- MODIFIED: This function now RETURNS base64 audio data ---
def text_to_speech_base64(text):
    """Generates TTS audio, encodes it to base64, and returns the string."""
    try:
        tts = gTTS.gTTS(text=text, lang='en-in')
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)
        
        # Encode the MP3 bytes to base64 for transmission
        audio_base64 = base64.b64encode(mp3_fp.read()).decode('utf-8')
        return audio_base64
    except Exception as e:
        print(f"Error in text_to_speech_base64: {e}")
        # Return an empty string on error
        return ""

# The original text_to_speech call was inside a thread. 
# We will now use a simple synchronous call since it's just generating bytes, 
# or keep the threading to prevent the gTTS latency from blocking the async loop.
# I'll modify the logic in handler to call it and await the result, 
# or use a simple synchronous call if the latency is acceptable. 
# Given the image processing time, a direct synchronous call is often simpler and fine.

async def handler(websocket):
    """
    Handles WebSocket connections and processes incoming frames for pose analysis.
    """
    client_id = id(websocket)
    print(f"Client {client_id} connected.")
    client_states[client_id] = {
        "current_asana_idx": 0,
        "hold_start_time": None,
        "last_feedback_time": 0,
        "asana_started": False
    }

    try:
        async for message in websocket:
            data = json.loads(message)
            image_data = data.get("imageData")
            
            # Placeholder for audio data to be sent
            audio_data_b64 = ""

            if not image_data:
                await websocket.send(json.dumps({"error": "Invalid data"}))
                continue

            state = client_states[client_id]

            # --- MODIFIED: Initial Asana Start TTS ---
            if not state["asana_started"]:
                audio_data_b64 = text_to_speech_base64("Starting Surya Namaskara sequence.")
                # Send the initial message and audio
                await websocket.send(json.dumps({"audio_data": audio_data_b64}))
                
                # Wait for the first speech to play out (client side)
                await asyncio.sleep(2) 

                current_pose_name = surya_namaskar_sequence[state['current_asana_idx']].replace('_', ' ')
                audio_data_b64 = text_to_speech_base64(f"First pose is {current_pose_name}")
                await websocket.send(json.dumps({"audio_data": audio_data_b64, "pose_name": current_pose_name}))
                state["asana_started"] = True
                continue # Skip processing the first frame until the client is ready

            # Decode the base64 image
            try:
                # ... (Image decoding logic remains the same)
                if ',' in image_data:
                    image_bytes = base64.b64decode(image_data.split(',')[1])
                else:
                    image_bytes = base64.b64decode(image_data)
                np_arr = np.frombuffer(image_bytes, np.uint8)
                frame = cv.imdecode(np_arr, cv.IMREAD_COLOR)
            except (base64.binascii.Error, IndexError) as e:
                await websocket.send(json.dumps({"error": f"Image decode error: {e}"}))
                continue

            # Find pose landmarks
            frame_with_pose = detector.findPose(frame)
            landmarks = detector.findPosition(frame_with_pose)

            pose_name = surya_namaskar_sequence[state['current_asana_idx']]

            if not landmarks:
                # Send a message with placeholder audio
                audio_data_b64 = text_to_speech_base64("Position unclear. Please move closer or try again.")
                await websocket.send(json.dumps({"data": 0, "confidence": 0, "pose_name": pose_name, "audio_data": audio_data_b64}))
                continue

            # Normalize landmarks
            normalized_landmarks = pose_similarity.normalize_landmarks(landmarks, reference_idx=0)

            # Check for similarity and accuracy
            is_similar, correct_landmarks = pose_similarity.isSimilar(pose_name, normalized_landmarks, 0.3)

            current_time = time.time()
            if current_time - state["last_feedback_time"] > 5: # Cooldown for feedback
                state["last_feedback_time"] = current_time
                
                # --- MODIFIED: Logic for generating TTS and including in response ---
                response_data = {}
                
                if is_similar:
                    accuracy = pose_similarity.accuracy(pose_name, normalized_landmarks, 30)
                    wrong_joints = pose_similarity.get_wrong_joints(pose_name, correct_landmarks, normalized_landmarks, 45)

                    if not wrong_joints:
                        if state["hold_start_time"] is None:
                            state["hold_start_time"] = time.time()
                        
                        elapsed = time.time() - state["hold_start_time"]
                        if elapsed >= 3: # Hold time
                            text = f"{pose_name.replace('_', ' ')} complete."
                            audio_data_b64 = text_to_speech_base64(text)
                            
                            state["current_asana_idx"] += 1
                            state["hold_start_time"] = None
                            
                            if state["current_asana_idx"] < len(surya_namaskar_sequence):
                                next_asana = surya_namaskar_sequence[state['current_asana_idx']].replace('_', ' ')
                                text = f"Next pose is {next_asana}"
                                # Generate a second audio for the next step, or just use the first one
                                audio_data_b64 += text_to_speech_base64(text) 
                                response_data = {"data": 4, "pose_name": next_asana} # 4 for next pose
                            else:
                                text = "Surya Namaskara complete. Well done."
                                audio_data_b64 = text_to_speech_base64(text)
                                response_data = {"data": 5} # 5 for sequence complete
                        else:
                            text = "Perfect pose! Hold it."
                            audio_data_b64 = text_to_speech_base64(text)
                            response_data = {"data": 2, "confidence": accuracy / 100, "pose_name": pose_name}
                    else:
                        state["hold_start_time"] = None
                        feedback_parts = []
                        for joint_key in wrong_joints:
                            joint_name = wrong_joints[joint_key][0]
                            change = wrong_joints[joint_key][1]
                            feedback_parts.append(f"{change} angle at {joint_name.replace('_', ' ')}")

                        feedback_text = ". ".join(feedback_parts[:2])
                        audio_data_b64 = text_to_speech_base64(feedback_text)
                        response_data = {"data": 3, "confidence": accuracy / 100, "pose_name": pose_name}
                else:
                    state["hold_start_time"] = None
                    text = "Adjust your position."
                    audio_data_b64 = text_to_speech_base64(text)
                    response_data = {"data": 1, "confidence": 0, "pose_name": pose_name}
                    
                # Final send with audio data
                response_data["audio_data"] = audio_data_b64
                await websocket.send(json.dumps(response_data))

    except websockets.exceptions.ConnectionClosed:
        print(f"Client {client_id} disconnected.")
    except Exception as e:
        print(f"An error occurred with client {client_id}: {e}")
        await websocket.send(json.dumps({"error": str(e)}))
    finally:
        if client_id in client_states:
            del client_states[client_id]


async def main():
    """
    Starts the WebSocket server.
    """
    # Using '0.0.0.0' is often safer than 'localhost' in WSL/network environments
    async with websockets.serve(handler, "0.0.0.0", 8765):
        print("WebSocket server started at ws://0.0.0.0:8765")
        await asyncio.Future() #Run forever

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Server stopped by KeyboardInterrupt.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")