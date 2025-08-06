import os
import tempfile
import subprocess
from werkzeug.utils import secure_filename

ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'flac'}

def allowed_audio_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AUDIO_EXTENSIONS

def convert_audio(file, output_format):
    filename = secure_filename(file.filename)
    input_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(input_path)

    name_only = os.path.splitext(filename)[0]
    output_filename = f"{name_only}.{output_format}"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)

    try:
        # FFMPEG command to convert audio file
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