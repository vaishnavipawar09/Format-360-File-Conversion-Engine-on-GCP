import os
import tempfile
from docx import Document
from PIL import Image, ImageDraw
from google.cloud import storage

# Initialize the Google Cloud Storage client
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

def docx_to_images(docx_path):
    """Converts a DOCX file to images, one image per page."""
    doc = Document(docx_path)
    images = []
    for i, para in enumerate(doc.paragraphs):
        img = Image.new('RGB', (800, 600), color = (255, 255, 255))
        d = ImageDraw.Draw(img)
        d.text((10,10), para.text, fill=(0,0,0))
        img_path = f"page_{i}.png"
        img.save(img_path)
        images.append(img_path)
    return images

def process_document(source_bucket_name, source_file_name, destination_bucket_name):
    """Process the document: download, convert to images, upload images."""
    temp_dir = tempfile.mkdtemp()
    local_docx_path = os.path.join(temp_dir, source_file_name)

    # Download the document from GCP
    download_blob(source_bucket_name, source_file_name, local_docx_path)

    # Convert the document to images
    image_paths = docx_to_images(local_docx_path)

    # Upload images to GCP
    for image_path in image_paths:
        upload_blob(destination_bucket_name, image_path, os.path.basename(image_path))

    # Cleanup local files
    os.remove(local_docx_path)
    for image_path in image_paths:
        os.remove(image_path)

# Example usage
source_bucket_name = 'format360_incomingfiles'
source_file_name = 'sample_doc.docx'
destination_bucket_name = 'format360_convertedfiles'
process_document(source_bucket_name, source_file_name, destination_bucket_name)
