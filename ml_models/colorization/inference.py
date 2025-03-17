import torch
from diffusers import StableDiffusionPipeline
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models/colorization/sd_model")

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe.to(device)

def colorize_image(image_path):
    """
    Colorizes the given grayscale image using Stable Diffusion.
    """
    from PIL import Image
    image = Image.open(image_path).convert("L")  # Convert to grayscale

    with torch.no_grad():
        colorized_image = pipe(image).images[0]

    output_path = os.path.join(settings.MEDIA_ROOT, "colorized_images")
    os.makedirs(output_path, exist_ok=True)

    colorized_image_path = os.path.join(output_path, os.path.basename(image_path))
    colorized_image.save(colorized_image_path)

    return os.path.relpath(colorized_image_path, settings.MEDIA_ROOT)  # Return relative path
