import cv2 as cv
import time
import PoseModule as pm
import threading
import pygame
import gtts as gTTS
import io
import warnings
import mediapipe as mp
import pose_equal_check as pec
import os
warnings.filterwarnings("ignore", category=UserWarning, module="google.protobuf.symbol_database")

# Initialize modules
Ideal_Poses = "D:/Sem_7/RK pe/Flexcellent/backend/ideal_poses"
detector = pm.PoseDetector()
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
PoseSimilarity = pec.PoseSimilarity()
pygame.mixer.init()

# ------------------ Text-to-speech function ------------------
# def text_to_speech(text):
#     """Play TTS audio asynchronously."""
#     try:
#         tts = gTTS.gTTS(text=text, lang='en-in')
#         mp3_fp = io.BytesIO()
#         tts.write_to_fp(mp3_fp)
#         mp3_fp.seek(0)
#         pygame.mixer.music.load(mp3_fp, 'mp3')
#         pygame.mixer.music.play()
#         while pygame.mixer.music.get_busy():
#             time.sleep(0.1)
#     except Exception as e:
#         print(f"Error in text_to_speech: {e}")

def text_to_speech(text):
    """Plays TTS audio without reinitializing pygame mixer."""
    try:
        # Convert the text to speech using gTTS (Google TTS)
        tts = gTTS.gTTS(text=text, lang='en-in')

        # Create an in-memory file for the speech
        mp3_fp = io.BytesIO()
        tts.write_to_fp(mp3_fp)
        mp3_fp.seek(0)

        # Play the speech using pygame
        pygame.mixer.music.load(mp3_fp, 'mp3')
        pygame.mixer.music.play()

        # Do not block the thread, check periodically
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

    except Exception as e:
        print(f"Error in text_to_speech: {e}")

# ------------------ Asana sequence ------------------
# surya_namaskar_sequence = [
#     "pranamasana",
#     "hastauttanasana",
#     "hastapadasana",
#     "right_ashwa_sanchalanasana",
#     "dandasana",
#     "ashtanga_namaskara",
#     "bhujangasana",
#     "adho_mukha_svanasana",
#     "left_ashwa_sanchalanasana",
#     "hastapadasana",
#     "hastauttanasana",
#     "pranamasana"
# ]

surya_namaskar_sequence = [
    
    "pranamasana",
    "hastauttanasana",

]

# ------------------ Function to perform sequence ------------------
def perform_asana_sequence(sequence, hold_time=3, similarity_threshold=0.1, wrong_angle_threshold=45):
    cap = cv.VideoCapture(0)
    current_asana_idx = 0
    hold_start_time = None
    last_feedback_time = 0
    feedback_cooldown = 5  # seconds between voice feedbacks

    text_to_speech("Starting Surya Namaskara sequence.")
    time.sleep(1)
    text_to_speech(f"First pose is {sequence[current_asana_idx].replace('_', ' ')}")

    while cap.isOpened() and current_asana_idx < len(sequence):
        ret, frame = cap.read()
        if not ret:
            print("❌ Camera not capturing frame.")
            break

        frame = cv.flip(frame, 1)
        frame = detector.findPose(frame)
        landmarks = detector.findPosition(frame)

        if len(landmarks) == 0:
            cv.putText(frame, "No pose detected!", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            cv.imshow("Yoga Trainer", frame)
            if cv.waitKey(1) & 0xFF == 27:
                break
            continue

        # Normalize landmarks
        landmarks = PoseSimilarity.normalize_landmarks(landmarks, reference_idx=0)
        pose_name = sequence[current_asana_idx]

        # Check pose similarity every few seconds
        current_time = time.time()
        if current_time - last_feedback_time > 5:  # limit frequency
            last_feedback_time = current_time

            isSimilar, correct_landmarks = PoseSimilarity.isSimilar(pose_name, landmarks, similarity_threshold)

            if isSimilar:
                wrong_joints = PoseSimilarity.get_wrong_joints(pose_name, correct_landmarks, landmarks, wrong_angle_threshold)
                if len(wrong_joints) == 0:
                    # Perfect pose detected
                    if hold_start_time is None:
                        hold_start_time = time.time()
                        text = f"Good. Hold {pose_name.replace('_', ' ')}"
                        threading.Thread(target=text_to_speech, args=(text,)).start()
                    else:
                        elapsed = time.time() - hold_start_time
                        cv.putText(frame, f"Holding... {elapsed:.1f}s", (20, 100), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        if elapsed >= hold_time:
                            text = f"{pose_name.replace('_', ' ')} complete."
                            # text_to_speech(f"{pose_name.replace('_', ' ')} complete.")
                            threading.Thread(target=text_to_speech, args=(text,)).start()
                            current_asana_idx += 1
                            hold_start_time = None
                            if current_asana_idx < len(sequence):
                                next_asana = sequence[current_asana_idx].replace('_', ' ')
                                text = f"Next pose is {next_asana}"
                                # text_to_speech(f"Next pose is {next_asana}")
                                threading.Thread(target=text_to_speech, args=(text,)).start()
                            else:
                                text = "Surya Namaskara complete. Well done."
                                # text_to_speech("Surya Namaskara complete. Well done.")
                                threading.Thread(target=text_to_speech, args=(text,)).start()
                                break
                else:
                    # Wrong joints feedback
                    hold_start_time = None
                    for joint in wrong_joints:
                        jname = wrong_joints[joint][0].replace('_', ' ')
                        direction = wrong_joints[joint][1]
                        text = f"{direction} angle at {jname}"
                        # text_to_speech(f"{direction} angle at {jname}")
                        threading.Thread(target=text_to_speech, args=(text,)).start()
            else:
                hold_start_time = None
                text = f"Adjust your pose. Try {pose_name.replace('_', ' ')} correctly."
                # text_to_speech(f"Adjust your pose. Try {pose_name.replace('_', ' ')} correctly.")
                threading.Thread(target=text_to_speech, args=(text,)).start()

        # # Display visuals
        # cv.putText(frame, f"Asana: {pose_name}", (20, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)

        # if current_time - last_feedback_time > 2:
        #     print("Hi")
        #     last_feedback_time = current_time

        ideal_image_path = os.path.join(Ideal_Poses, f"{pose_name}.jpg")
        ideal_pose_img = cv.imread(ideal_image_path)
        if ideal_pose_img is not None:
            cv.imshow("Reference Pose", ideal_pose_img)

        cv.imshow("Yoga Trainer", frame)
        if cv.waitKey(1) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv.destroyAllWindows()


# ------------------ MAIN ------------------
if __name__ == "__main__":
    perform_asana_sequence(
        surya_namaskar_sequence,
        hold_time=3,              # seconds to hold correct pose
        similarity_threshold=0.3, # how close the pose must be
        wrong_angle_threshold=60  # angle tolerance
    )
