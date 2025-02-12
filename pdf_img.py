import os
import tempfile
from pdf2image import convert_from_path
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

def convert_pdf_to_images(pdf_file_path):
    """Converts a PDF file to a list of images."""
    return convert_from_path(pdf_file_path)

def process_pdf(source_bucket_name, pdf_file_name, destination_bucket_name):
    """Process the PDF: download, convert to images, upload images."""
    temp_dir = tempfile.mkdtemp()
    local_pdf_path = os.path.join(temp_dir, pdf_file_name)

    # Download the PDF from GCP
    download_blob(source_bucket_name, pdf_file_name, local_pdf_path)

    # Convert the PDF to images
    images = convert_pdf_to_images(local_pdf_path)

    # Upload images to GCP
    for i, image in enumerate(images):
        image_path = os.path.join(temp_dir, f"image_{i}.png")
        image.save(image_path, 'PNG')
        upload_blob(destination_bucket_name, image_path, os.path.basename(image_path))

    # Cleanup local files
    os.remove(local_pdf_path)
    for image in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, image))
    os.rmdir(temp_dir)

# Example usage
source_bucket_name = 'format360_incomingfiles'
pdf_file_name = 'AUX_invoice.pdf'
destination_bucket_name = 'format360_convertedfiles'
process_pdf(source_bucket_name, pdf_file_name, destination_bucket_name)
