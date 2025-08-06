import os
import tempfile
from werkzeug.utils import secure_filename
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation

from pdf2docx import Converter as PDF2DOCXConverter
from docx2pdf import convert as docx_to_pdf

ALLOWED_DOCUMENT_EXTENSIONS = {'pdf', 'docx', 'txt', 'pptx'}

def allowed_document_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_DOCUMENT_EXTENSIONS

def convert_document(file, input_format, output_format):
    filename = secure_filename(file.filename)
    input_path = os.path.join(tempfile.gettempdir(), filename)
    file.save(input_path)

    name_only = os.path.splitext(filename)[0]
    output_filename = f"{name_only}.{output_format}"
    output_path = os.path.join(tempfile.gettempdir(), output_filename)

    try:
        # PDF → DOCX
        if input_format == "pdf" and output_format == "docx":
            cv = PDF2DOCXConverter(input_path)
            cv.convert(output_path)
            cv.close()

        # DOCX → PDF
        elif input_format == "docx" and output_format == "pdf":
            docx_to_pdf(input_path, output_path)

        # DOCX → TXT
        elif input_format == "docx" and output_format == "txt":
            doc = Document(input_path)
            text = '\n'.join([para.text for para in doc.paragraphs])
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)

        # TXT → DOCX
        elif input_format == "txt" and output_format == "docx":
            with open(input_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            doc = Document()
            for line in lines:
                doc.add_paragraph(line.strip())
            doc.save(output_path)

        # PDF → TXT
        elif input_format == "pdf" and output_format == "txt":
            reader = PdfReader(input_path)
            text = ''
            for page in reader.pages:
                text += page.extract_text() + '\n'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)

        # PPTX → PDF or TXT (simple extract)
        elif input_format == "pptx" and output_format == "txt":
            prs = Presentation(input_path)
            text = ''
            for slide in prs.slides:
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text += shape.text + '\n'
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(text)
        else:
            return None, "Unsupported conversion."
        
        return output_path, None
    except Exception as e:
        return None, str(e)
    finally:
        os.remove(input_path)