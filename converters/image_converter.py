import os
import tempfile
from PIL import Image
from werkzeug.utils import secure_filename

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}

def allowed_image_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def convert_image(file, output_format):
    filename = secure_filename(file.filename)
    input_ext = filename.rsplit('.', 1)[1].lower()

    # Temporary input path
    input_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(input_path)

    name_only = os.path.splitext(filename)[0]
    output_filename = f"{name_only}.{output_format}"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)

    try:
        image = Image.open(input_path).convert("RGB")
        image.save(output_path, format=output_format.upper())
        return output_path, None
    except Exception as e:
        return None, str(e)
    finally:
        os.remove(input_path)