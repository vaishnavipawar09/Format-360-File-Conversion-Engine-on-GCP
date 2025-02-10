from flask import Flask, request, jsonify, render_template, url_for
from google.cloud import storage
import os
import uuid
import logging
from datetime import timedelta

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Initialize Google Cloud Storage client using the environment variable
# The GOOGLE_APPLICATION_CREDENTIALS environment variable must be set in your deployment environment
storage_client = storage.Client()
#storage_client = storage.Client('C:\\Users\\vpvai\\OneDrive\\Documents\\ECC Project\\format-360-f58b24ed953d.json')


source_bucket_name = 'new-format360-incomingfiles'
converted_bucket_name = 'format360_convertedfiles'

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        unique_id = uuid.uuid4().hex
        original_extension = os.path.splitext(file.filename)[1]
        unique_filename = f"{unique_id}_{file.filename}".replace(original_extension, '')
        #converted_filename = f"{uuid.uuid4().hex}.pdf"  # Assuming conversion to PDF
        #unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        converted_filename = f"{unique_filename}"
        unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
        logging.info(f"Uploading file {unique_filename} to bucket {source_bucket_name}")
        blob = storage_client.bucket(source_bucket_name).blob(unique_filename)
        try:
            blob.upload_from_file(file.stream, content_type=file.content_type)
            logging.info("Upload successful")
            download_url = url_for('download', filename=unique_filename, _external=True)
            return jsonify({'message': 'File uploaded successfully', 'filename': unique_filename, 'download_url': download_url})
        except Exception as e:
            logging.error(f"Failed to upload file: {e}", exc_info=True)
            return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>', methods=['GET'])
def download(filename):
    try:
        bucket = storage_client.bucket(converted_bucket_name)
        blob = bucket.blob(filename)

        if not blob.exists():
            logging.error(f"File {filename} not found in bucket {converted_bucket_name}")
            return jsonify({'error': 'File not found'}), 404

        # Set the expiration time for the signed URL
        expiration_time = timedelta(minutes=5)

        # Generate the signed URL for direct file download
        signed_url = blob.generate_signed_url(expiration=expiration_time, method='GET')
        logging.info(f"Generated signed URL for file {filename}")
        return jsonify({'signed_url': signed_url})
    except Exception as e:
        logging.error(f"Failed to download file: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=True, host='0.0.0.0', port=port)
