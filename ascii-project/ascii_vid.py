import cv2 
from PIL import Image
import numpy as np
from pathlib import Path

from main import resize_image, grayify, pixels_to_ascii, ASCII_CHARS, fixed_width

def frame_to_ascii(frame, max_width=fixed_width):
    image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    image = resize_image(image, max_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)
    width, _ = image.size

    ascii_image = "\n".join(
        ascii_str[i:i+width] for i in range(0, len(ascii_str), width)
    )
    return ascii_image

def video_to_ascii(video_path, width=fixed_width, fps_limit=None):
    cap = cv2.VideoCapture(str(video_path))

    if not cap.isOpened():
        raise FileNotFoundError(f"Cannot open video file: {video_path}")
    
    while True: 
        ret, frame= cap.read()
        if not ret:
            break
        ascii_frame = frame_to_ascii(frame, width)

        print("\033c", end="")
        print(ascii_frame)

        if fps_limit:
            cv2.waitKey(int(1000 / fps_limit))
        else:
            cv2.waitKey(1)
    cap.release()

if __name__ == "__main__":
    video_to_ascii("video.mp4", width=150, fps_limit=30)