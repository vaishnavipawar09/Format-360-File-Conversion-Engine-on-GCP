from google.cloud import storage

# Explicitly set credentials
storage_client = storage.Client.from_service_account_json(r'C:\Users\Vaishnavi\Documents\Lectures\ECC\Ecc_proj\format-360-f58b24ed953d.json')



import os
import tempfile
from google.cloud import storage
import fitz  # PyMuPDF
from docx import Document

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

# Specify the bucket and file name
source_bucket_name = 'format360_incomingfiles'
source_file_name = 'sample_pdf.pdf'

# Use a temporary directory for storing the PDF file
temp_dir = os.path.join(os.getcwd(), "temp")  # Create a "temp" directory within the current working directory
os.makedirs(temp_dir, exist_ok=True)  # Create the directory if it doesn't exist
local_pdf = os.path.join(temp_dir, "sample_pdf.pdf")

download_blob(source_bucket_name, source_file_name, local_pdf)

# Conversion process
pdf_document = fitz.open(local_pdf)
doc = Document()
for page_num in range(len(pdf_document)):
    page = pdf_document.load_page(page_num)
    text = page.get_text("text")
    doc.add_paragraph(text)

# Close the PDF document
pdf_document.close()

# Save the DOCX locally
local_docx = os.path.join(temp_dir, "output.docx")
doc.save(local_docx)

# Upload the DOCX to a different bucket
destination_bucket_name = 'format360_convertedfiles'
destination_file_name = 'output.docx'
upload_blob(destination_bucket_name, local_docx, destination_file_name)

# Cleanup local files if necessary
try:
    os.remove(local_pdf)
except PermissionError:
    print(f"Could not delete {local_pdf}. File is being used by another process.")
try:
    os.remove(local_docx)
except PermissionError:
    print(f"Could not delete {local_docx}. File is being used by another process.")