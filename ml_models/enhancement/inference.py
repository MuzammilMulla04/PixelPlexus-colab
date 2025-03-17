import torch
from diffusers import StableDiffusionPipeline
import os
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models/enhancement/sd_model")

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe.to(device)

def enhance_image(image_path):
    """
    Enhances the given image using Stable Diffusion.
    """
    from PIL import Image
    image = Image.open(image_path).convert("RGB")

    with torch.no_grad():
        enhanced_image = pipe(image).images[0]

    output_path = os.path.join(settings.MEDIA_ROOT, "enhanced_images")
    os.makedirs(output_path, exist_ok=True)

    enhanced_image_path = os.path.join(output_path, os.path.basename(image_path))
    enhanced_image.save(enhanced_image_path)

    return os.path.relpath(enhanced_image_path, settings.MEDIA_ROOT)  # Return relative path
