from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
from exceptions import ModelLoadError, CaptionGenerationError

class CaptionService:
    """Service for generating captions from images."""

    def __init__(self):
        try:
            self.processor = AutoProcessor.from_pretrained("microsoft/git-base-coco")
            self.model = AutoModelForCausalLM.from_pretrained("microsoft/git-base-coco")
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
            pixel_values = self.processor(images=image, return_tensors="pt").pixel_values
            generated_ids = self.model.generate(pixel_values, max_length=50)
            caption = self.processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
            return caption
        except Exception as e:
            raise CaptionGenerationError("Failed to generate caption") from e
