import cv2
import numpy as np


# init part
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
params = cv2.SimpleBlobDetector_Params()

params.filterByArea = True
params.maxArea = 1500
params.filterByCircularity = True
params.minCircularity = 0.5

# Set up the detector with default parameters.
detector = cv2.SimpleBlobDetector_create(params)


def detect_faces(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    coords = cascade.detectMultiScale(gray_frame, 1.3, 5)
    if len(coords) > 1:
        biggest = (0, 0, 0, 0)
        for i in coords:
            if i[3] > biggest[3]:
                biggest = i
        biggest = np.array([i], np.int32)
    elif len(coords) == 1:
        biggest = coords
    else:
        return None
    for (x, y, w, h) in biggest:
        frame = img[y:y + h, x:x + w]
    return frame


def detect_eyes(img, cascade):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = cascade.detectMultiScale(gray_frame, 1.3, 5)  # detect eyes
    width = np.size(img, 1)  # get face frame width
    height = np.size(img, 0)  # get face frame height
    left_eye = None
    right_eye = None
    for (x, y, w, h) in eyes:
        if y > height / 2:
            pass
        eyecenter = x + w / 2  # get the eye center
        if eyecenter < width * 0.5:
            left_eye = img[y:y + h, x:x + w]
        else:
            right_eye = img[y:y + h, x:x + w]
    return left_eye, right_eye


def cut_eyebrows(img):
    height, width = img.shape[:2]
    eyebrow_h = int(height / 4)
    img = img[eyebrow_h:height, 0:width]  # cut eyebrows out (15 px)

    return img


def blob_process(img, threshold, detector):
    gray_frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # _, img = cv2.threshold(gray_frame, threshold, 255, cv2.THRESH_BINARY)
    # img = cv2.erode(img, None, iterations=2)
    # img = cv2.dilate(img, None, iterations=4)
    # img = cv2.medianBlur(img, 5)
    keypoints = detector.detect(gray_frame)
    return keypoints


def nothing(x):
    pass


def track(img, threshold):
    ###################################################

    # FIX THIS SECTION
    # img is the input image of the face. This function should return the image that is output on the screen

    ###################################################
    face_frame = detect_faces(img, face_cascade)
    eye = None
    if face_frame is not None:
        eyes = detect_eyes(face_frame, eye_cascade)
        for eye in eyes:
            if eye is not None:
                eye = cut_eyebrows(eye)
                keypoints = blob_process(eye, threshold, detector)
                eye = cv2.drawKeypoints(eye, keypoints, eye, (0, 0, 255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
                # # return fraction of the eye image that keypoint is in
                # w = len(eye)
                # fraction = keypoints[0].pt[0]/w
                # fractions.append(fraction)
    # return 0 if eye is left, 1 otherwise
    return eye


