import torch
import os
from PIL import Image
from diffusers import StableDiffusionUpscalePipeline
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "ml_models/enhancement/sd_model")

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionUpscalePipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
pipe.to(device)

def enhance_image(image_file, user_prompt=None):
    """
    Enhances the given image using Stable Diffusion upscaling.
    - image_file: File-like object (InMemoryUploadedFile).
    - user_prompt: Optional custom enhancement prompt.
    """

    # Load and preprocess image directly from InMemoryUploadedFile
    input_image = Image.open(image_file).convert("RGB").resize((256, 256))

    with torch.inference_mode():
        upscaled_image = pipe(
            prompt="high quality, detailed, realistic" if user_prompt is None else user_prompt,
            image=input_image,
            num_inference_steps=50,
            guidance_scale=7.5
        ).images[0]

    # Save enhanced image
    output_dir = os.path.join(settings.MEDIA_ROOT, "enhanced_images")
    os.makedirs(output_dir, exist_ok=True)

    enhanced_image_path = os.path.join(output_dir, image_file.name)
    upscaled_image.save(enhanced_image_path)

    return os.path.relpath(enhanced_image_path, settings.MEDIA_ROOT)  # Return relative path for Django
