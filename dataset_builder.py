import argparse
import sys
import time
from datetime import datetime
from pathlib import PurePath
import random

import cv2
from notify import notification


def capture_frame(path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        sys.exit('Could not open video camera')
    ret, frame = cap.read()
    cv2.imwrite(path, frame)
    cap.release()


def make_file_path(save_dir, label):
    file_name = '{}_{}.png'.format(label, datetime.now().strftime('%Y_%m_%d_%H:%M'))
    return str(PurePath(save_dir) / file_name)


def main():
    parser = argparse.ArgumentParser(
        description='Generates data set to train i3-eye by periodically capturing from the '
                    'camera. Will capture every minute until process is killed')
    parser.add_argument('--dest', required=True, help='destination directory where to save '
                                                      'captured images. The name of the images '
                                                      'will be a date time stamp')
    flags = parser.parse_args()

    warning_time = 3
    down_time = 58
    focus_left = random.choice([True, False])

    while True:
        notification(f"Capture in {warning_time} seconds. Look "
                     f"{'LEFT' if focus_left else 'RIGHT'}")
        time.sleep(warning_time)
        capture_frame(make_file_path(flags.dest, 'L' if focus_left else 'R'))
        focus_left = not focus_left

        time.sleep(down_time)


if __name__ == '__main__':
    main()
