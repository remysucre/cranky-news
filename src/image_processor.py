import io
import requests
from PIL import Image
import base64


MAX_WIDTH = 300  # Reduced from 400 to keep image data smaller
MAX_HEIGHT = 180  # Reduced from 240 to keep image data smaller


def download_image(url):
    """Download image from URL and return PIL Image object."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content))
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None


def resize_image(img, max_width=MAX_WIDTH, max_height=MAX_HEIGHT):
    """Resize image to fit within max dimensions while preserving aspect ratio."""
    width, height = img.size

    # Calculate scaling factor
    width_ratio = max_width / width
    height_ratio = max_height / height
    scale = min(width_ratio, height_ratio, 1.0)  # Don't upscale

    if scale < 1.0:
        new_width = int(width * scale)
        new_height = int(height * scale)
        return img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return img


def atkinson_dither(img):
    """Apply Atkinson dithering algorithm to convert to 1-bit monochrome.
    Atkinson dithering produces a lighter, more detailed result ideal for displays."""
    # Convert to grayscale first
    img = img.convert('L')

    # Convert to a format we can manipulate
    pixels = img.load()
    width, height = img.size

    # Create a copy as float for error diffusion
    pixel_array = [[pixels[x, y] for x in range(width)] for y in range(height)]

    # Atkinson dithering
    for y in range(height):
        for x in range(width):
            old_pixel = pixel_array[y][x]
            new_pixel = 255 if old_pixel > 127 else 0
            pixel_array[y][x] = new_pixel

            # Atkinson diffuses only 3/4 of the error (loses 1/4)
            error = (old_pixel - new_pixel) / 8.0

            # Distribute error to neighboring pixels (Atkinson pattern)
            if x + 1 < width:
                pixel_array[y][x + 1] += error
            if x + 2 < width:
                pixel_array[y][x + 2] += error

            if y + 1 < height:
                if x > 0:
                    pixel_array[y + 1][x - 1] += error
                pixel_array[y + 1][x] += error
                if x + 1 < width:
                    pixel_array[y + 1][x + 1] += error

            if y + 2 < height:
                pixel_array[y + 2][x] += error

    # Convert back to PIL Image
    result = Image.new('1', (width, height))
    result_pixels = result.load()

    for y in range(height):
        for x in range(width):
            result_pixels[x, y] = 1 if pixel_array[y][x] > 127 else 0

    return result


def image_to_particle_pixels(img):
    """Convert 1-bit PIL Image to particle pixel format string."""
    width, height = img.size
    pixels = img.load()

    lines = []
    for y in range(height):
        line = ''
        for x in range(width):
            # In PIL Image mode '1', 0 is black, 255/1 is white
            # In particle format, 0 is white, 1 is black
            pixel_value = pixels[x, y]
            line += '0' if pixel_value else '1'
        lines.append(line)

    return ' '.join(lines)


def process_and_save_image(url, output_path, max_width=MAX_WIDTH, max_height=MAX_HEIGHT):
    """
    Download, process an image to particle format, and save to a file.
    Returns True if successful, False otherwise.
    """
    import json

    img = download_image(url)
    if img is None:
        return False

    # Resize to fit Playdate screen
    img = resize_image(img, max_width, max_height)

    # Convert to RGBA to handle transparency, then to RGB
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Apply dithering
    img = atkinson_dither(img)

    width, height = img.size

    # Convert to particle pixel format
    pixels = image_to_particle_pixels(img)

    # Create particle document for the image
    particle_doc = {
        'format': 'particle',
        'title': 'Image',
        'content': [{
            'type': 'image',
            'width': width,
            'height': height,
            'pixels': pixels,
            'style': {
                'scale': 1,
                'margin-top': 8,
                'margin-bottom': 8
            }
        }]
    }

    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(particle_doc, f, indent=2, ensure_ascii=False)

    return True
