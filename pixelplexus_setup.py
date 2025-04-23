# File 1: pixelplexus_setup.py
import os
import subprocess

def run_command(cmd, use_shell=True):
    print(f"💻 Running: {cmd}")
    subprocess.run(cmd, shell=use_shell, check=True)

def setup_pixelplexus():
    print("🔹 Setting up Node.js 18...")
    run_command("curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -")
    run_command("apt-get update && apt-get install -y python3-pip")
    run_command("sudo apt-get install -y nodejs")

    print("🔹 Installing Python packages...")
    run_command("pip install django django-tailwind numpy pandas matplotlib django-browser-reload")
    run_command("pip install diffusers transformers accelerate torch torchvision torchaudio pyngrok")

    print("🔹 Cloning GitHub repository...")
    GITHUB_USERNAME = "MuzammilMulla04"
    REPO_NAME = "PixelPlexus-colab"
    GITHUB_TOKEN = "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"

    REPO_PATH = f"/content/{REPO_NAME}"
    run_command(f"git clone https://{GITHUB_USERNAME}:{GITHUB_TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git {REPO_PATH}")
    os.chdir(REPO_PATH)

    print("🔹 Pulling latest updates from GitHub...")
    run_command("git pull")

    print("🔹 Setting up Stable Diffusion models...")
    from diffusers import StableDiffusionPipeline, StableDiffusionUpscalePipeline

    models = {
        "generation": {
            "model": "stabilityai/stable-diffusion-2-1",
            "path": "ml_models/generation/sd_model",
            "loader": StableDiffusionPipeline
        },
        "enhancement": {
            "model": "stabilityai/stable-diffusion-x4-upscaler",
            "path": "ml_models/enhancement/sd_model",
            "loader": StableDiffusionUpscalePipeline
        }
    }

    for name, config in models.items():
        print(f"  → Loading and saving model for {name}...")
        pipe = config["loader"].from_pretrained(config["model"])
        pipe.save_pretrained(config["path"])
        print(f"  ✅ {name.capitalize()} model saved to {config['path']}")

    print("🎉 All models downloaded and saved successfully~!")

if __name__ == "__main__":
    setup_pixelplexus()