import os
import sys
import django
import subprocess
from django.core.management import call_command
from pyngrok import ngrok

# Ensure the script runs from the correct directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(BASE_DIR)

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PixelPlexus.settings")  # Update with your project name
django.setup()

def run_command(cmd):
    """Runs a shell command and handles errors."""
    result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"❌ Error in command: {cmd}")
        print(result.stderr)
    else:
        print(f"✅ {cmd} executed successfully.")

def setup_django():
    """Automates Django setup."""

    print("🔹 Applying Migrations...")
    call_command("makemigrations")
    call_command("makemigrations", "base")
    call_command("migrate")

    print("🔹 Creating Superuser...")
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@gmail.com", "adminpass")
        print("✅ Superuser created.")
    else:
        print("✅ Superuser already exists.")

    print("🔹 Installing & Starting Tailwind...")
    run_command("python manage.py tailwind install")
    run_command("python manage.py tailwind start")

    print("🔹 Setting up Ngrok for public access...")
    NGROK_AUTH_TOKEN = "your-ngrok-auth-token"  # Replace with your actual Ngrok token
    run_command(f"ngrok authtoken {NGROK_AUTH_TOKEN}")

    PORT = 8000
    public_url = ngrok.connect(PORT).public_url
    print(f"🔹 Public URL: {public_url}")

    print("🔹 Running Django Server...")
    run_command("python manage.py runserver 0.0.0.0:8000 > server_log.txt 2>&1 &")

    print("✅ Django Setup Completed Successfully! 🎉")

if __name__ == "__main__":
    setup_django()
