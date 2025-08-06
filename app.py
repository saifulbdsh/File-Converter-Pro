from flask import Flask, render_template, request, send_file, redirect, url_for, Response
import os
from datetime import datetime
from converters.document_converter import convert_document, allowed_document_file
from converters.image_converter import convert_image, allowed_image_file
from converters.audio_converter import convert_audio, allowed_audio_file
from converters.video_converter import convert_video, allowed_video_file

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html', year=datetime.now().year)

# Routes for static pages
@app.route('/about')
def about():
    return render_template('about.html', year=datetime.now().year)

@app.route('/privacy')
def privacy():
    return render_template('privacy.html', year=datetime.now().year)

@app.route('/terms')
def terms():
    return render_template('terms.html', year=datetime.now().year)

# Dynamic sitemap route for SEO
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    urls = []
    now = datetime.now().strftime('%Y-%m-%d')
    
    # Static pages with their properties
    urls.append({'loc': 'https://fileconverterpro.xyz/', 'lastmod': now, 'changefreq': 'daily', 'priority': '1.0'})
    urls.append({'loc': 'https://fileconverterpro.xyz/about', 'lastmod': now, 'changefreq': 'monthly', 'priority': '0.8'})
    urls.append({'loc': 'https://fileconverterpro.xyz/privacy', 'lastmod': now, 'changefreq': 'yearly', 'priority': '0.5'})
    urls.append({'loc': 'https://fileconverterpro.xyz/terms', 'lastmod': now, 'changefreq': 'yearly', 'priority': '0.5'})
    
    sitemap_xml = render_template('sitemap.xml', urls=urls)
    
    return Response(sitemap_xml, mimetype='application/xml')

@app.route('/convert/document', methods=['POST'])
def convert_doc():
    file = request.files.get("file")
    output_format = request.form.get("output_format")
    if not file or not allowed_document_file(file.filename):
        return "Invalid document file", 400
    input_ext = file.filename.rsplit('.', 1)[1].lower()
    converted_path, error = convert_document(file, input_ext, output_format)
    if error:
        return f"Error: {error}", 500
    return send_file(converted_path, as_attachment=True)

@app.route('/convert/image', methods=['POST'])
def convert_image_route():
    file = request.files.get("file")
    output_format = request.form.get("output_format")
    if not file or not allowed_image_file(file.filename):
        return "Invalid image file", 400
    converted_path, error = convert_image(file, output_format)
    if error:
        return f"Error: {error}", 500
    return send_file(converted_path, as_attachment=True)

@app.route('/convert/audio', methods=['POST'])
def convert_audio_route():
    file = request.files.get("file")
    output_format = request.form.get("output_format")
    if not file or not allowed_audio_file(file.filename):
        return "Invalid audio file", 400
    converted_path, error = convert_audio(file, output_format)
    if error:
        return f"Error: {error}", 500
    return send_file(converted_path, as_attachment=True)

@app.route('/convert/video', methods=['POST'])
def convert_video_route():
    file = request.files.get("file")
    output_format = request.form.get("output_format")
    if not file or not allowed_video_file(file.filename):
        return "Invalid video file", 400
    converted_path, error = convert_video(file, output_format)
    if error:
        return f"Error: {error}", 500
    return send_file(converted_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)