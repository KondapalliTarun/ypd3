import numpy as np
import cv2 as cv
import mediapipe as mp
import numpy as np
import time
import PoseModule as pm
# Initialize MediaPipe Pose Detection
import ideal_landmarks_data
import absolutely_ideal_landmarks_data
import os

import sys
from pathlib import Path

script_dir = Path(__file__).parent
Ideal_Poses = script_dir / "ideal_poses"
ideal_landmarks = ideal_landmarks_data.ideal_landmarks
absolutely_ideal_landmarks = absolutely_ideal_landmarks_data.absolutely_ideal_landmarks
detector = pm.PoseDetector()
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils
asana_to_joint = detector.map_asana_joints()
ctime =0
ptime = time.time()

class PoseSimilarity():
    # Function to calculate Euclidean distance between two points
    def euclidean_distance(self, point1, point2):
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    # # Function to normalize key points based on a reference point
    # def normalize_landmarks(self, landmarks, reference_idx):
    #     ref_point = landmarks[reference_idx]
    #     normalized_landmarks = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in landmarks]
    #     return normalized_landmarks
    
    def normalize_landmarks(self, landmarks, reference_idx):
        if landmarks is None or len(landmarks) == 0:
            return []
        if reference_idx >= len(landmarks):
            return landmarks  # return as-is if index invalid

        ref_point = landmarks[reference_idx]
        normalized_landmarks = [(point[0] - ref_point[0], point[1] - ref_point[1]) for point in landmarks]
        return normalized_landmarks


    # Function to compare two sets of pose landmarks
    # def compare_poses(self, landmarks1, landmarks2, threshold=0.1):
    #     total_distance = 0
    #     for i in range(len(landmarks1)):
    #         total_distance += self.euclidean_distance(landmarks1[i], landmarks2[i])
    #     avg_distance = total_distance / len(landmarks1)
    #     return avg_distance
    
    def compare_poses(self, landmarks1, landmarks2, threshold=0.1):
        if landmarks1 is None or landmarks2 is None:
            return float('inf')
        if len(landmarks1) == 0 or len(landmarks2) == 0:
            return float('inf')  # return large distance if empty

        total_distance = 0
        for i in range(len(landmarks1)):
            total_distance += self.euclidean_distance(landmarks1[i], landmarks2[i])

        avg_distance = total_distance / len(landmarks1)
        return avg_distance

    
    def get_wrong_joints(self, asana, correct_landmarks, input_landmarks, thresh):
        correct_landmark_dict = detector.map_landmarks(correct_landmarks)
        correct_joints_dict = detector.map_joints(correct_landmark_dict)
        correct_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,correct_joints_dict)

        input_landmark_dict = detector.map_landmarks(input_landmarks)
        input_joints_dict = detector.map_joints(input_landmark_dict)
        input_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,input_joints_dict)

        wrong_joints = {}
        for i in correct_joints_dict:
            correct_angle = detector.calculate_angle(correct_joints_dict[i])
            input_angle = detector.calculate_angle(input_joints_dict[i])
            print(f"Correct angle is {correct_angle} and the input angle is {input_angle}.")
            diff = correct_angle - input_angle
            if(abs(diff)>thresh):
                if(diff>0):
                    wrong_joints[i] =  (i, "increase")
                else:
                    wrong_joints[i] = (i, "decrease")
        return wrong_joints
    
    def accuracy(self, asana, input_landmarks, thresh):
        image_path = str(Ideal_Poses / f"{asana}.jpg")
        ideal_asana = cv.imread(image_path)
        if ideal_asana is None:
            print(f"Error: Ideal pose image not found for {asana} at {image_path}")
            return 0.0

        ideal_image_frame = detector.findPose(ideal_asana)
        correct_landmarks = detector.findPosition(ideal_image_frame)
        correct_landmarks = self.normalize_landmarks(correct_landmarks, reference_idx=0)

        correct_landmark_dict = detector.map_landmarks(correct_landmarks)
        correct_joints_dict = detector.map_joints(correct_landmark_dict)
        correct_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,correct_joints_dict)

        input_landmark_dict = detector.map_landmarks(input_landmarks)
        input_joints_dict = detector.map_joints(input_landmark_dict)
        input_joints_dict=detector.get_joints_for_asana(asana,asana_to_joint,input_joints_dict)

        # correct_angles = {}
        # ideal_angles = {}
        total_score = 0
        valid_joints = 0
        for i in correct_joints_dict:
            user_angle = detector.calculate_angle(correct_joints_dict[i])
            ideal_angle = detector.calculate_angle(input_joints_dict[i])

            angle_diff = abs(user_angle - ideal_angle)
            normalized_error = max(0, 1 - (angle_diff / thresh))  # within ±tolerance
            total_score += normalized_error
            valid_joints += 1

        if valid_joints == 0:
            return 0.0

        accuracy = (total_score / valid_joints) * 100
        return round(accuracy, 2)
        


    # def isSimilar(self, pose_name, input_landmarks, euclidean_threshold):
        # correct_landmarks = ideal_landmarks[pose_name] + absolutely_ideal_landmarks[pose_name]
        mini = float('inf')
        closest_landmarks = []
        flag = 0
        
        # Load ideal pose image
        image_path = os.path.join("Ideal_Poses", f"{pose_name}.jpg")
        ideal_asana = cv.imread(image_path)
        if ideal_asana is None:
            print(f"Error: Ideal pose image not found for {pose_name} at {image_path}")
            return (False, {})


        ideal_image_frame = detector.findPose(ideal_asana)
        correct_landmarks = detector.findPosition(ideal_image_frame)
        correct_landmarks = self.normalize_landmarks(correct_landmarks, reference_idx=0)

        for i in correct_landmarks:
            dist = self.compare_poses(i, input_landmarks, euclidean_threshold)
            if(dist<euclidean_threshold):
                print("You're doing it right.")
                flag = 1
            if(dist<mini):
                mini = dist
                closest_landmarks = i
        
        if(flag):
            return (True, closest_landmarks)
        else:            
            return (False, closest_landmarks)
        #return self.get_wrong_joints(pose_name, closest_landmarks, input_landmarks, angular_threshold)

    def isSimilar(self, pose_name, input_landmarks, euclidean_threshold):
        mini = float('inf')
        closest_landmarks = []
        flag = 0

        image_path = str(Ideal_Poses / f"{pose_name}.jpg")
        ideal_asana = cv.imread(image_path)
        if ideal_asana is None:
            print(f"Error: Ideal pose image not found for {pose_name} at {image_path}")
            return (False, [])

        ideal_image_frame = detector.findPose(ideal_asana)
        correct_landmarks = detector.findPosition(ideal_image_frame)
        correct_landmarks = self.normalize_landmarks(correct_landmarks, reference_idx=0)

        # Compare full sets of landmarks, not individual ones
        dist = self.compare_poses(correct_landmarks, input_landmarks, euclidean_threshold)

        if dist < euclidean_threshold:
            print("Pose is similar")
            flag = 1
            closest_landmarks = correct_landmarks
        else:
            mini = dist
            closest_landmarks = correct_landmarks

        return (flag == 1, closest_landmarks)

        

def resize_image(image, max_width=800, max_height=600):
    height, width = image.shape[:2]
    if width > max_width or height > max_height:
        scaling_factor = min(max_width / width, max_height / height)
        new_size = (int(width * scaling_factor), int(height * scaling_factor))
        return cv.resize(image, new_size)
    return image



if __name__ == "__main__":
    # Initialize pose detector and accuracy evaluator
    detector = pm.PoseDetector()
    PoseSimilarity = PoseSimilarity()

    # Choose asana name and image paths
    asana = "pranamasana"
    ideal_image_path = "D:/Sem_7/RK pe/Flexcellent/backend/ideal_poses/pranamasana.jpg"
    user_image_path = "D:/Sem_7/RK pe/Flexcellent/backend/ideal_poses/pranamasana.jpg"

    # Read images
    ideal_img = cv.imread(ideal_image_path)
    user_img = cv.imread(user_image_path)

    if ideal_img is None or user_img is None:
        print("❌ Error: Could not read one or both images. Check file paths.")
        exit()

    # Detect pose and landmarks
    ideal_img = detector.findPose(ideal_img)
    correct_landmarks = detector.findPosition(ideal_img)
    correct_landmarks = PoseSimilarity.normalize_landmarks(correct_landmarks, 0)

    user_img = detector.findPose(user_img)
    input_landmarks = detector.findPosition(user_img)
    input_landmarks = PoseSimilarity.normalize_landmarks(input_landmarks, 0)

    if len(correct_landmarks) == 0 or len(input_landmarks) == 0:
        print("❌ Pose not detected in one of the images.")
        exit()

    # Compute accuracy
    thresh = 15  # angular tolerance in degrees
    accuracy = PoseSimilarity.accuracy(asana, input_landmarks, thresh)

    # Print and display
    print(f"✅ Accuracy score for {asana}: {accuracy}%")

    cv.imshow("Ideal Pose", ideal_img)
    cv.imshow("User Pose", user_img)
    cv.waitKey(0)
    cv.destroyAllWindows()

