import torch
import os
from PIL import Image
from diffusers import StableDiffusionUpscalePipeline
from django.conf import settings

MODEL_PATH = os.path.join(settings.BASE_DIR, "/ml_models/enhancement/sd_model")

device = "cuda" if torch.cuda.is_available() else "cpu"

pipe = StableDiffusionUpscalePipeline.from_pretrained(MODEL_PATH, torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
pipe.to(device)

def enhance_image(image_path, user_prompt= None):
    """
    Enhances the given image using Stable Diffusion upscaling.
    - image_path: Path to the input image.
    - num_inference_steps: Number of inference steps (higher = better quality, slower).
    - guidance_scale: Strength of enhancement (default 7.5, lower = subtle, higher = aggressive).
    """
    try:
        # Load and preprocess image
        input_image = Image.open(image_path).convert("RGB").resize((256, 256))  # Resize for stable diffusion input
        
        with torch.inference_mode():
            upscaled_image = pipe(
                prompt="high quality, detailed, realistic" if not user_prompt else user_prompt,
                image=input_image,
                num_inference_steps=50,
                guidance_scale=7.5
            ).images[0]

        # Save enhanced image
        output_dir = os.path.join(settings.MEDIA_ROOT, "enhanced_images")
        os.makedirs(output_dir, exist_ok=True)

        enhanced_image_path = os.path.join(output_dir, os.path.basename(image_path))
        upscaled_image.save(enhanced_image_path)

        return os.path.join(settings.MEDIA_URL, "enhanced_images", os.path.basename(image_path))

    except Exception as e:
        print(f"Error during enhancement: {e}")
        return None
