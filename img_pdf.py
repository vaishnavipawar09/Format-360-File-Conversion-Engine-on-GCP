
from google.cloud import storage
from PIL import Image
import os

# Explicitly set credentials
storage_client = storage.Client.from_service_account_json(r"C:\Users\shrey\OneDrive\Documents\ECC\format-360-c1acb273d5b4.json")
from google.cloud import storage
from docx import Document
from reportlab.pdfgen import canvas
import tempfile


# Initialize the Google Cloud Storage client
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
source_file_name = 'AUX_invoice_page-0001.jpg'
"""local_image_path = "/tmp/AUX_invoice_page-0001.jpg"
download_blob(source_bucket_name, source_file_name, local_image_path)"""

# Use a temporary directory for storing the files
temp_dir = tempfile.gettempdir()
local_image_path = os.path.join(temp_dir, "AUX_invoice_page-0001.jpg")

download_blob(source_bucket_name, source_file_name, local_image_path)

# Convert the image to PDF
image = Image.open(local_image_path)
rgb_image = image.convert('RGB')  # Convert to RGB mode if not already
local_pdf_path = os.path.join(temp_dir, "img.pdf")
rgb_image.save(local_pdf_path)

# Upload the PDF to the destination bucket
destination_bucket_name = 'format360_convertedfiles'
destination_file_name = 'img.pdf'
upload_blob(destination_bucket_name, local_pdf_path, destination_file_name)

# Cleanup local files if necessary
os.remove(local_image_path)
os.remove(local_pdf_path)


