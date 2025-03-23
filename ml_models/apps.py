from django.apps import AppConfig
import torch
from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline, StableDiffusionControlNetPipeline, ControlNetModel

class MLModelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ml_models'

    def ready(self):
        """Load all three models once on Django startup."""
        from django.conf import settings

        model_paths = {
            "generation": "/content/PixelPlexus-colab/ml_models/generation/sd_model",
            "enhancement": "/content/PixelPlexus-colab/ml_models/enhancement/sd_model",
            "colorization": "/content/PixelPlexus-colab/ml_models/colorization/sd_model",
        }

        device = "cuda" if torch.cuda.is_available() else "cpu"

        # Load each model and store in settings
        settings.GENERATION_PIPELINE = StableDiffusionPipeline.from_pretrained(
            model_paths["generation"], torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)
        print("✅ Stable Diffusion Generation Model Loaded!")

        settings.ENHANCEMENT_PIPELINE = StableDiffusionUpscalePipeline.from_pretrained(
            model_paths["enhancement"], torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)
        print("✅ Stable Diffusion Enhancement Model Loaded!")

        controlnet = ControlNetModel.from_pretrained("lllyasviel/sd-controlnet-mlsd")  # Load ControlNet for colorization
        settings.COLORIZATION_PIPELINE = StableDiffusionControlNetPipeline.from_pretrained(
            model_paths["colorization"], controlnet=controlnet, torch_dtype=torch.float16 if device == "cuda" else torch.float32
        ).to(device)
        print("✅ Stable Diffusion Colorization Model Loaded!")
