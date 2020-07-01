from binary_utils import from_bits
import collections
import requests
import json
import re
import os

PROJECT_DIR = r'D:\SmartTv'
CIRCLES_PATH = r'circles'
API_KEY = '***************'


def ocr_space_file(filename, overlay=False, api_key=API_KEY, language='eng'):
    """
    OCR.space API request with local file.
    :param filename: Your file path & name.
    :param overlay: Is OCR.space overlay required in your response.
    :param api_key: OCR.space API key.
    :param language: Language code to be used in OCR.
    :return: Result in JSON format.
    """

    payload = {'isOverlayRequired': overlay,
               'apikey': api_key,
               'language': language,
               'OCREngine': 2,
               'detectOrientation': True
               }

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={filename: f},
                          data=payload,
                          )

    return json.loads(r.content.decode())['ParsedResults'][0]['ParsedText']


def detect_bits():
    """
    Detect bits in circles
    """
    bits = {}

    for root, dirs, files in os.walk(os.path.join(PROJECT_DIR, CIRCLES_PATH), topdown=False):
        for file in files:
            if file.endswith(".jpg"):
                try:
                    file_number = int(re.findall(r'\d+', file)[0])
                    bits[file_number] = int(ocr_space_file(os.path.join(PROJECT_DIR, CIRCLES_PATH, file)))
                    print("File: " + file + " Number: " + str(file_number) + " Bit: " + str(bits[file_number]))
                except (ValueError, IndexError):
                    print("File: " + file + " Bit not found")

    ordered = collections.OrderedDict(sorted(bits.items()))
    return [v for k, v in ordered.items()]


if __name__ == "__main__":
    result_bits = detect_bits()
    print(result_bits)
    print(from_bits(result_bits))
