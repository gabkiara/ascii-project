import os 
import random
import shutil
from pathlib import Path

from PIL import Image

ASCII_CHARS = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,`'. "
fixed_width = 200

def pick_image(folder: Path) -> Path:
    exts = ['.png', '.jpg', '.jpeg', '.bmp', '.gif']
    images = [p for p in folder.iterdir() if p.suffix.lower() in exts]

    if not images:
        raise FileNotFoundError("No images found in the specified folder.")
    
    return random.choice(images)

def resize_image(image: Image.Image, new_width=int) -> Image.Image:
    width, height = image.size
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * 0.55)
    return image.resize((new_width, max(1, new_height)))

def grayify(image: Image.Image) -> Image.Image:
    return image.convert("L")

def pixels_to_ascii(image: Image.Image) -> str:
    pixels = image.getdata()
    chars = "".join(
        ASCII_CHARS[pixel * len(ASCII_CHARS) // 256] for pixel in pixels
    )
    return chars 

def image_to_ascii(image_path: Path, max_width: int = fixed_width) -> str:
    image = Image.open(image_path)

    image = resize_image(image, max_width)
    image = grayify(image)

    ascii_str = pixels_to_ascii(image)

    pixel_count = len(ascii_str)
    width, _ = image.size
    ascii_image ="\n".join(
        ascii_str[i : i + width] for i in range(0, pixel_count, width)
    )
    return ascii_image

def main():
    base_dir = Path(__file__).parent
    images_dir = base_dir / "images"

    random_image = pick_image(images_dir)
    print(f"Selected image: {random_image.name}\n")

    ascii_art = image_to_ascii(random_image)
    print(ascii_art)    

if __name__ == "__main__":
    main()
