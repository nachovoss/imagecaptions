import io
import os
import app
import unittest
import requests
from PIL import Image
from dotenv import load_dotenv
from caption_service import CaptionService

load_dotenv()

TEST_IMAGE_PATH = os.getenv('TEST_IMAGE_PATH')


class TestImageCaptioningApp(unittest.TestCase):

    def setUp(self):
        app.app.testing = True
        self.client = app.app.test_client()


    def test_caption_endpoint_with_no_file(self):
        response = self.client.post('/caption')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part', response.json['error'])


    def test_caption_endpoint_with_invalid_file(self):
        data = {
            'file': (io.BytesIO(b"not an image"), 'test.txt')
        }
        response = self.client.post('/caption', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid file type', response.json['error'])


    def test_caption_endpoint_with_valid_file(self):
        # Assuming there's a valid test image in the directory
        with open(TEST_IMAGE_PATH, 'rb') as img:
            img_bytes = io.BytesIO(img.read())
        
        data = {
            'file': (img_bytes, 'test.jpg')
        }
        response = self.client.post('/caption', content_type='multipart/form-data', data=data)
        self.assertEqual(response.status_code, 200)
        print(response.json)
        # Check if the response contains a caption (the exact content will depend on the model)
        self.assertIn('caption', response.json)


class TestImageCaptioningAppIntegration(unittest.TestCase):
    
    BASE_URL = 'http://127.0.0.1:5000'

    def test_caption_endpoint_with_no_file(self):
        response = requests.post(f'{self.BASE_URL}/caption')
        self.assertEqual(response.status_code, 400)
        self.assertIn('No file part', response.json()['error'])
    

    def test_caption_endpoint_with_invalid_file(self):
        data = {
            'file': (io.BytesIO(b"not an image"))
        }
        response = requests.post(f'{self.BASE_URL}/caption', files=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid file type', response.json()['error'])
    

    def test_caption_endpoint_with_valid_file(self):
        with open(TEST_IMAGE_PATH, 'rb') as img:
            files = {'file': ('test.jpg', img)}
            response = requests.post(f"{self.BASE_URL}/caption", files=files)
            self.assertEqual(response.status_code, 200)
            self.assertIn('caption', response.json())


class TestCaptionService(unittest.TestCase):

    def setUp(self):
        self.service = CaptionService()

    def test_generate_caption_with_valid_image(self):
        with open(TEST_IMAGE_PATH, 'rb') as img:
            image = Image.open(io.BytesIO(img.read()))

        caption = self.service.generate_caption(image)
        self.assertIsInstance(caption, str)


if __name__ == '__main__':
    unittest.main()