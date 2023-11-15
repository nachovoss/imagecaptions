import os
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
    """Checks if a file is allowed based on its extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.errorhandler(ModelLoadError)
@app.errorhandler(CaptionGenerationError)
def handle_caption_error(error):
    """Handles caption errors.
    Args:
        error (exceptions.CaptionError): The error to handle.
    """
    logging.error(f"Caption Error: {error}")
    return make_response(jsonify({"error": str(error)}), 500)


@app.errorhandler(BadRequest)
def handle_bad_request(error):
    """Handles bad requests.
    Args:
        error (werkzeug.exceptions.BadRequest): The error to handle.
    """
    logging.warning(f"Bad Request: {error}")
    return make_response(jsonify({"error": "Bad Request: " + str(error)}), 400)


@app.route('/caption', methods=['POST'])
def caption_image():
    """ Generates a caption from an image.
     Returns:
        json: The generated caption.
     Raises:
        BadRequest: If the request is invalid.
        CaptionError: If caption generation fails.
    """
    if 'file' not in request.files:
        logging.warning("No file part in the request")
        return make_response(jsonify({"error": "No file part"}), 400)

    file = request.files['file']
    if file.filename == '':
        logging.warning("No file selected")
        return make_response(jsonify({"error": "No selected file"}), 400)

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        try:
            file.save(filepath)
            with Image.open(filepath) as image:
                caption = caption_service.generate_caption(image)
            os.remove(filepath)  # Cleanup file
            return make_response(jsonify({"caption": caption}))
        except CaptionError as e:
            logging.error(f"Caption generation failed: {e}")
            return make_response(jsonify({"error": str(e)}), 500)
        except IOError:
            logging.error("Invalid image format")
            return make_response(jsonify({"error": "Invalid image format"}), 400)
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    else:
        logging.warning("Invalid file type")
        return make_response(jsonify({"error": "Invalid file type"}), 400)


if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)  # Set debug=False in production
