from video_processing import split_to_frames
from data_detection import detect_frames
from data_processing import detect_bits
from binary_utils import from_bits


def main():
    split_to_frames()
    detect_frames()
    result = detect_bits()

    try:
        print(from_bits(result))
    except ValueError:
        print("Could not parse result data")


if __name__ == "__main__":
    main()
