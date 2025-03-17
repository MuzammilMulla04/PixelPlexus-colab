import os
from diffusers import StableDiffusionPipeline
import torch

# Load the model
pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5").to("cuda")  # Use GPU if available

# Define the base directory for saving images
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # Gets PixelPlexus root
SAVE_DIR = os.path.join(BASE_DIR, "media", "generated_images")

# Ensure the directory exists
os.makedirs(SAVE_DIR, exist_ok=True)

# Define function for text-to-image generation
def generate_image(prompt, filename="generated.png"):
    """Generates an image and saves it to the media folder."""
    image = pipe(prompt).images[0]  # Generate image
    save_path = os.path.join(SAVE_DIR, filename)  # Construct full path
    image.save(save_path)  # Save output
    return save_path

# Example usage
prompt = "A futuristic cyberpunk cityscape at night"
generated_path = generate_image(prompt, "cyberpunk.png")
print(f"Image saved at: {generated_path}")
