import os
import cv2
import numpy as np
import fnmatch

PROJECT_DIR = r'D:\SmartTv'
FRAMES_PATH = r'frames'
CIRCLES_PATH = r'circles'
FILE_NAME = 'frame'


def detect_frames():
    """
    Detect circles in frames
    """
    number_of_frames = len(fnmatch.filter(os.listdir(os.path.join(PROJECT_DIR, FRAMES_PATH)), '*.jpg'))

    for i in range(number_of_frames):
        if (i % 2) == 0:
            try:
                detect_frame(FILE_NAME + str(i) + '.jpg')
            except (ValueError, cv2.error):
                try:
                    if (i + 1) <= (number_of_frames - 1):
                        detect_frame(FILE_NAME + str(i + 1) + '.jpg')
                except (ValueError, cv2.error):
                    print("Failed to found circle: %d" % i)


def detect_frame(file_name):
    """
    Detect frame
    :param file_name: image name
    """
    file_path = os.path.join(PROJECT_DIR, FRAMES_PATH, file_name)
    cur_image = cv2.imread(file_path)
    copy = cur_image.copy()
    gray = cv2.cvtColor(copy, cv2.COLOR_BGR2GRAY)
    detect_circles(file_name, gray)


def detect_circles(file_name, image):
    """
    Detect circles in image
    :param file_name: file name
    :param image: cv2 image
    """
    circles = cv2.HoughCircles(image, cv2.HOUGH_GRADIENT, 1.2, 100)

    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        (x, y, r) = circles[0]

        rect_x = (x - r)
        rect_y = (y - r)
        crop_img = image[rect_y:(rect_y + 2 * r), rect_x:(rect_x + 2 * r)]

        cv2.imwrite(os.path.join(PROJECT_DIR, CIRCLES_PATH, 'circle_' + file_name), crop_img)
        print(file_name)
    else:
        raise ValueError


if __name__ == "__main__":
    detect_frames()
