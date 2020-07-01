import os
import cv2

PROJECT_DIR = r'D:\SmartTv'
VIDEO_PATH = r'video\data.mp4'
FRAMES_PATH = r'frames'


def split_to_frames():
    """
    Split video to frames
    """
    video = cv2.VideoCapture(os.path.join(PROJECT_DIR, VIDEO_PATH))
    success, image = video.read()
    count = 0

    while success:
        video.set(cv2.CAP_PROP_POS_MSEC, (count * 1075))
        cv2.imwrite(os.path.join(PROJECT_DIR, FRAMES_PATH, "frame%d.jpg") % count, image)
        success, image = video.read()
        print('Read frame %d' % count)
        count += 1


if __name__ == "__main__":
    split_to_frames()
