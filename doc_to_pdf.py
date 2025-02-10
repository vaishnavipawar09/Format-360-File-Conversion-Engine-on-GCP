import os
from google.cloud import storage
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import tempfile

def convert_file(event, context):
    """Triggered by a change to a Google Cloud Storage bucket."""
    # Initializes client
    storage_client = storage.Client()

    # Get the file that has been uploaded to GCS
    bucket_name = event['bucket']
    file_name = event['name']
    blob = storage_client.bucket(bucket_name).blob(file_name)

    # Setup temporary file for processing
    _, temp_local_filename = tempfile.mkstemp()
    blob.download_to_filename(temp_local_filename)

    # Conversion logic
    doc = Document(temp_local_filename)
    output = tempfile.NamedTemporaryFile(delete=False, suffix='.pdf')
    pdf = canvas.Canvas(output.name, pagesize=letter)
    y_position = letter[1] - 72
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text:
            if y_position < 72:
                pdf.showPage()
                y_position = letter[1] - 72
            pdf.drawString(72, y_position, text)
            y_position -= 15
    pdf.save()

    # Upload the converted file to the converted bucket
    converted_bucket = storage_client.bucket('format360_convertedfiles')
    new_blob = converted_bucket.blob(file_name.replace('.docx', '.pdf'))
    new_blob.upload_from_filename(output.name)

    # Cleanup temporary files
    os.remove(temp_local_filename)
    os.remove(output.name)

    print(f"Processed file {file_name} and uploaded to {converted_bucket.name}")