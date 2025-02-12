from google.cloud import storage
from PIL import Image
from docx import Document
import os
import tempfile

# Explicitly set credentials
storage_client = storage.Client.from_service_account_json(r"C:\Users\shrey\OneDrive\Documents\ECC\format-360-c1acb273d5b4.json")

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

def image_to_doc(image_path, doc_path):
    """Converts an image file to a .docx file with the image embedded."""
    doc = Document()
    doc.add_picture(image_path)  # Adds the image to the document
    doc.save(doc_path)
    print(f"Document saved to {doc_path}")

# Specify the bucket and file names
source_bucket_name = 'format360_incomingfiles'
source_file_name = 'AUX_invoice_page-0001.jpg'

# Use a temporary directory for storing the files
temp_dir = tempfile.gettempdir()
local_image_path = os.path.join(temp_dir, source_file_name)
local_doc_path = os.path.join(temp_dir, "output.docx")

# Download the image from the bucket
download_blob(source_bucket_name, source_file_name, local_image_path)

# Convert the image to a Word document
image_to_doc(local_image_path, local_doc_path)

# Upload the Word document to the destination bucket
destination_bucket_name = 'format360_convertedfiles'
destination_file_name = 'img_to_doc.docx'
upload_blob(destination_bucket_name, local_doc_path, destination_file_name)

# Cleanup local files if necessary
os.remove(local_image_path)
os.remove(local_doc_path)
