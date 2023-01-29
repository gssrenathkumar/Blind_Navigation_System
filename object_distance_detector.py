import cv2
from playsound import playsound

# Distance is calculated from the previous image in inches type
Known_distance = 30
Known_width = 5.7

# Taking maximum threshold
thres = 0.45

# Data Configuratioons files
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'
# Getting the words from the coco.names file and right striping it
classNames = []
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = [line.rstrip() for line in f]

# CV2 Detection model with the Configuration Files
net = cv2.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 320)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

# Colors  >>> BGR Format(BLUE, GREEN, RED)
GREEN = (0, 255, 0)
RED = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (0, 255, 255)
WHITE = (255, 255, 255)
CYAN = (255, 255, 0)
MAGENTA = (255, 0, 242)
GOLDEN = (32, 218, 165)
LIGHT_BLUE = (255, 9, 2)
PURPLE = (128, 0, 128)
CHOCOLATE = (30, 105, 210)
PINK = (147, 20, 255)
ORANGE = (0, 69, 255)

# Taking top fonts
fonts = cv2.FONT_HERSHEY_COMPLEX
fonts2 = cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
fonts3 = cv2.FONT_HERSHEY_COMPLEX_SMALL
fonts4 = cv2.FONT_HERSHEY_TRIPLEX

# Camera Object
cap = cv2.VideoCapture(0)  # Taking 0 for getting primary camera footage
Distance_level = 0

# face detector object
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


# Calculating the distance between the lens and live taken image imported
def FocalLength(measured_distance, real_width, width_in_rf_image):
    """Calculating the focal length by finding the width of the face and measuring from the endpoint"""
    focal_length = (width_in_rf_image * measured_distance) / real_width
    return focal_length


# distance estimation function
# Estimating the distance between the object and the camera
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):
    """ Calculating the distance from the lens to the user or objects accurately"""
    distance = (real_face_width * Focal_Length) / face_width_in_frame
    return distance


# Live Face Detection Feed
# This function helps to detect face and draw rectangle on the screen
def face_data(image, CallOut, Distance_level):
    """Create a face mapping of circles and text on the live feed camera"""
    face_width = 0
    face_x, face_y = 0, 0
    face_center_x = 0
    face_center_y = 0
    # Getting the graysscale live feed
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray_image, 1.3, 5)
    # Detecing face and creating a live in all 4 direction
    for (x, y, w, h) in faces:
        line_thickness = 2
        LLV = int(h * 0.12)
        cv2.line(image, (x, y + LLV), (x + w, y + LLV), (GREEN), line_thickness)
        cv2.line(image, (x, y + h), (x + w, y + h), (GREEN), line_thickness)
        cv2.line(image, (x, y + LLV), (x, y + LLV + LLV), (GREEN), line_thickness)
        cv2.line(
            image, (x + w, y + LLV), (x + w, y + LLV + LLV), (GREEN), line_thickness
        )
        cv2.line(image, (x, y + h), (x, y + h - LLV), (GREEN), line_thickness)
        cv2.line(image, (x + w, y + h), (x + w, y + h - LLV), (GREEN), line_thickness)

        face_width = w
        face_center = []
        # Creating a circle shape on the screen on live data feed
        face_center_x = int(w / 2) + x
        face_center_y = int(h / 2) + y
        if Distance_level < 10:
            Distance_level = 10

        if CallOut == True:
            cv2.line(image, (x, y - 11), (x + 180, y - 11), (ORANGE), 28)
            cv2.line(image, (x, y - 11), (x + 180, y - 11), (YELLOW), 20)
            cv2.line(image, (x, y - 11), (x + Distance_level, y - 11), (GREEN), 18)
    return face_width, faces, face_center_x, face_center_y


# Getting the reference image to calculate the focal and distance level length
ref_image = cv2.imread("Ref_image.jpg")

# Calculating the distance focal length like a training data from the distance between camera and user
ref_image_face_width, _, _, _ = face_data(ref_image, False, Distance_level)
Focal_length_found = FocalLength(Known_distance, Known_width, ref_image_face_width)
print(Focal_length_found)

# Capturing live feed from Videocapture function in which 0 is taken as primary camera
while True:
    _, frame = cap.read()
    classIds, confs, bbox = net.detect(frame, confThreshold=thres)
    face_width_in_frame, Faces, FC_X, FC_Y = face_data(frame, True, Distance_level)
    # finding the distance by calling function Distance finder
    for (face_x, face_y, face_w, face_h) in Faces:
        if face_width_in_frame != 0:
            # Calculating the distance ,detecting face and finally drawing a circle shape for it
            Distance = Distance_finder(
                Focal_length_found, Known_width, face_width_in_frame
            )
            Distance = round(Distance, 2)
            # Creating rectangle box and adding text like distance and object name
            Distance_level = int(Distance)
            # Printing the text on the live camera feed
            cv2.putText(
                frame,
                f"Distance {Distance} Inches",
                (face_x - 6, face_y - 6),
                fonts,
                0.5,
                (BLACK),
                2,
            )
            if Distance < 25:
                playsound("beep.mp3")
                # Detecting objects and detecting objects distance finally printing it
            if len(classIds) != 0:
                for classId, confidence, box in zip(classIds.flatten(), confs.flatten(), bbox):
                    cv2.putText(frame, classNames[classId - 1].upper(), (box[0] + 10, box[1] + 30),
                                cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("frame", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
