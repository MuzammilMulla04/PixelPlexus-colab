import torch
from diffusers import StableDiffusionPipeline
import os
from django.conf import settings

# Load Stable Diffusion model
MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models/generation/sd_model")

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionPipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe.to(device)

def generate_image(prompt):
    """
    Generates an image from the given text prompt using Stable Diffusion.
    """
    with torch.no_grad():
        image = pipe(prompt).images[0]

    # Save the generated image
    output_path = os.path.join(settings.MEDIA_ROOT, "generated_images")
    os.makedirs(output_path, exist_ok=True)
    
    image_path = os.path.join(output_path, f"{hash(prompt)}.png")
    image.save(image_path)

    return os.path.relpath(image_path, settings.MEDIA_ROOT)  # Return relative path for Django
