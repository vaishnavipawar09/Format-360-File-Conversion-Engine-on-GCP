#doc_to_pdf.py

from google.cloud import storage
# Explicitly set credentials
storage_client = storage.Client.from_service_account_json(r"C:\Users\shrey\OneDrive\Documents\ECC\format-360-c1acb273d5b4.json")
from google.cloud import storage
from docx import Document
from reportlab.pdfgen import canvas
import os
import tempfile

# Initialize Google Cloud Storage client
storage_client = storage.Client()
def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Blob {source_blob_name} downloaded to {destination_file_name}.")
def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")
# Specify the bucket and file names
source_bucket_name = 'format360_incomingfiles'
source_file_name = 'ECC ASSIGNMENT 2_Report.docx'

# Use a temporary directory for storing the files
temp_dir = tempfile.gettempdir()
local_docx = os.path.join(temp_dir, "ECC ASSIGNMENT 2_Report.docx")

download_blob(source_bucket_name, source_file_name, local_docx)

# Conversion process (basic text extraction and PDF creation)
doc = Document(local_docx)
local_pdf = os.path.join(temp_dir, "ECC_output_doc.pdf")
c = canvas.Canvas(local_pdf)
for paragraph in doc.paragraphs:
    c.drawString(72, 800, paragraph.text)  # Simple text writing to PDF; adjust positioning as needed
    c.showPage()  # Add a page break for each paragraph; adjust logic for more sophisticated formatting
c.save()

# Upload the PDF to a different bucket
destination_bucket_name = 'format360_convertedfiles'
destination_file_name = 'output_doc.pdf'
upload_blob(destination_bucket_name, local_pdf, destination_file_name)

# Cleanup local files if necessary
os.remove(local_docx)
os.remove(local_pdf)