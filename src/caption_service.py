import re
import os
from PIL import Image
from dotenv import load_dotenv
from transformers import AutoProcessor, AutoModelForCausalLM
from exceptions import ModelLoadError, CaptionGenerationError

load_dotenv()

MODEL = os.getenv("MODEL")


class CaptionService:
    """Service for generating captions from images."""

    def __init__(self):
        try:
            self.processor = AutoProcessor.from_pretrained(MODEL)
            self.model = AutoModelForCausalLM.from_pretrained(MODEL)
        except Exception as e:
            raise ModelLoadError("Failed to load the model and processor") from e

    def generate_caption(self, image):
        """Generates a caption from an image.
        Args:
            image (PIL.Image): The image to generate a caption for.
        Returns:
            str: The generated caption.
        Raises:
            TypeError: If the image is not a PIL image.
            CaptionGenerationError: If caption generation fails.
        """
        if not isinstance(image, Image.Image):
            raise TypeError("Image must be a PIL image")
        try:

            prompt = "what is this?"
            inputs = self.processor(
                        prompt,
                        image,
                        return_tensors="pt",
                        max_length=64
                    )

            sample = self.model.generate(**inputs, max_length=64)
            caption = self.processor.tokenizer.decode(sample[0]).replace(prompt, "")
            pattern = r"\[(SEP|CLS)\]"
            caption = re.sub(pattern, "", caption).strip().capitalize()
            return caption

        except Exception as e:
            raise CaptionGenerationError("Failed to generate caption") from e
