import cv2 as cv

# --- Load the reference image ---
reference = cv.imread('ideal_poses\pranamasana.jpg')
if reference is None:
    print("Error: Reference image not found!")
    exit()

# --- Open your webcam (0 = default camera) ---
cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # --- Read a frame from webcam ---
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not read frame.")
        break

    # --- Display both windows ---
    cv.imshow("Live Stream", frame)
    cv.imshow("Reference Pose", reference)

    # --- Press 'q' to quit ---
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# --- Release resources ---
cap.release()
cv.destroyAllWindows()
