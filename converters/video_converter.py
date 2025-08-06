import os
import tempfile
import subprocess
from werkzeug.utils import secure_filename

ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv', 'webm'}

def allowed_video_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def convert_video(file, output_format):
    filename = secure_filename(file.filename)
    input_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(input_path)

    name_only = os.path.splitext(filename)[0]
    output_filename = f"{name_only}.{output_format}"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)

    try:
        command = [
            'ffmpeg',
            '-i', input_path,
            output_path
        ]
        
        subprocess.run(command, check=True, capture_output=True, text=True)
        return output_path, None
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg Error: {e.stderr}")
        return None, f"FFmpeg Error: {e.stderr}"
    except Exception as e:
        return None, str(e)
    finally:
        os.remove(input_path)