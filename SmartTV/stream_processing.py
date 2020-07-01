import time
import cv2
import os
import datetime
import urllib.request
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from multiprocessing import Manager, Process

STREAM_URL = 'http://*.*.*.*:8080/video/mjpeg'
SNAPSHOT_EVERY_X_SECONDS = 1.075
SNAPSHOT_OUTPUT = "frame%d.jpg"
SEGMENT_EVERY_X_SECONDS = 21
SEGMENT_OUTPUT = "cam1_{timestamp}.mp4"
PROJECT_DIR = r'D:\SmartTv'
FRAMES_PATH = r'frames'


# Init
stream = urllib.request.urlopen(STREAM_URL)
bytes = bytes()
img_array = []
font_path = "FreeSans.ttf"
font = ImageFont.truetype(font_path, 16)
last_ts_snapshot = 0
last_ts_segment = 0
i = 0


def process_frames(video_name, frames):

    height, width, layers = frames[0].shape
    out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), len(frames) / SEGMENT_EVERY_X_SECONDS, (width, height))

    for i in range(len(frames)):
        out.write(frames[i])

    out.release()


if __name__ == "__main__":
    frame = 0

    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            i += 1
            # print("frame " + str(i))
            jpg = bytes[a:b+2]
            bytes = bytes[b+2:]
            image = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)
            # image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
            cv2.rectangle(image, (0, 0), (170, 20), (255, 255, 255), -1)
            img_pil = Image.fromarray(image)
            draw = ImageDraw.Draw(img_pil)
            ts = time.time()
            st = datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y %H:%M:%S')
            draw.text((10, 0), st, font=font, fill=(0, 0, 0, 1))
            image = np.array(img_pil)
            img_array.append(image)

            if ts - last_ts_snapshot >= SNAPSHOT_EVERY_X_SECONDS:
                print("Prepare snapshot")
                cv2.imwrite(os.path.join(PROJECT_DIR, FRAMES_PATH, SNAPSHOT_OUTPUT) % frame, image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                last_ts_snapshot = ts
                frame += 1

            # if (ts - last_ts_segment) >= SEGMENT_EVERY_X_SECONDS:
            #         tsmark = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H-%M-%S')
            #         video_name = SEGMENT_OUTPUT.replace('{timestamp}', tsmark)
            #         print("Prepare video " + video_name)
            #         p = Process(target=process_frames, args=(video_name, img_array))
            #         p.start()
            #         img_array = []
            #         last_ts_segment = ts

            # cv2.imshow('i', image)
            # if cv2.waitKey(1) == 27:
            # 	break
