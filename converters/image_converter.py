import os
import tempfile
from werkzeug.utils import secure_filename
from PIL import Image

# Supported image formats
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp', 'bmp', 'tiff'}

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def convert_image(file, output_format):
    try:
        filename = secure_filename(file.filename)
        input_path = os.path.join(tempfile.gettempdir(), filename)
        file.save(input_path)

        name_only = os.path.splitext(filename)[0]
        output_filename = f"{name_only}.{output_format}"
        output_path = os.path.join(tempfile.gettempdir(), output_filename)

        with Image.open(input_path) as img:
            if output_format == "jpg":
                img = img.convert("RGB")  # JPG doesn't support transparency
            img.save(output_path, output_format.upper())

        return output_path, None
    except Exception as e:
        return None, f"Image conversion error: {str(e)}"
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
