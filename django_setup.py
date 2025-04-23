# File 2: django_setup.py
import os
import subprocess

def run_command(cmd, use_shell=True):
    print(f"💻 Running: {cmd}")
    subprocess.run(cmd, shell=use_shell, check=True)

def setup_django_tailwind():
    print("🎀 Tailwind Setup Starting...")
    run_command("python manage.py tailwind init")
    user_input = input("🌸 Done updating settings.py manually? Press 'y' to continue: ")
    while user_input.strip().lower() != 'y':
        user_input = input("⚠️ Please press 'y' to continue after editing settings.py: ")
    run_command("python manage.py tailwind install")
    run_command("python manage.py tailwind start &")

def setup_django_db():
    print("🛠️ Django DB Setup...")
    run_command("python manage.py makemigrations")
    run_command("python manage.py makemigrations base")
    run_command("python manage.py migrate")
    print("👤 Creating Django superuser...")
    run_command("echo \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@example.com', 'adminpass') if not User.objects.filter(username='admin').exists() else print('Superuser exists')\" | python manage.py shell")

def main():
    setup_django_tailwind()
    setup_django_db()

if __name__ == "__main__":
    main()