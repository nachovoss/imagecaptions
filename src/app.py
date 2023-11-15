import os
import asyncio
from flask import Flask, request, jsonify, make_response
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from PIL import Image
from caption_service import CaptionService
from exceptions import CaptionError, ModelLoadError, CaptionGenerationError
import logging

load_dotenv()

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
caption_service = CaptionService()

UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
ALLOWED_EXTENSIONS = set(os.getenv('ALLOWED_EXTENSIONS', 'png,jpg,jpeg').split(','))
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # Default 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.errorhandler(ModelLoadError)
@app.errorhandler(CaptionGenerationError)
def handle_caption_error(error):
    logging.error(f"Caption Error: {error}")
    return make_response(jsonify({"error": str(error)}), 500)

@app.errorhandler(BadRequest)
def handle_bad_request(error):
    logging.warning(f"Bad Request: {error}")
    return make_response(jsonify({"error": "Bad Request: " + str(error)}), 400)

async def async_generate_caption(image_path):
    try:
        with Image.open(image_path) as image:
            caption = await asyncio.to_thread(caption_service.generate_caption, image)
        return caption
    finally:
        if os.path.exists(image_path):
            os.remove(image_path)

@app.route('/caption', methods=['POST'])
async def caption_image():
    if 'file' not in request.files:
        handle_bad_request("No file part in the request")
    
    file = request.files['file']

    if file.filename == '':
        handle_bad_request("No file selected")    

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        try:
            caption = await async_generate_caption(filepath)
            return make_response(jsonify({"caption": caption}))
        except CaptionError as e:
            handle_caption_error(f"Caption generation failed: {e}")
        except IOError as e:
             logging.warning(f"Bad Request: {e}")
             return make_response(jsonify({"error": "Bad Request: " + str(e)}), 400)
            
    else:
        logging.warning("Invalid file type")
        return make_response(jsonify({"error": "Invalid file type"}), 400)

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True, use_reloader=False)  # Set debug=False in production
