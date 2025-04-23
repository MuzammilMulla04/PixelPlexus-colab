# File 3: run_pixelplexus_server.py
import os
import subprocess
from pyngrok import ngrok
import threading
import time

def run_command(cmd, use_shell=True):
    print(f"💻 Running: {cmd}")
    subprocess.run(cmd, shell=use_shell, check=True)

def stream_logs(file_path):
    with open(file_path, 'r') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if line:
                print(line.strip())
            else:
                time.sleep(0.5)

def run_server():
    print("🚀 Running Django Server...")
    run_command("fuser -k 8000/tcp || true")
    run_command("ngrok authtoken 2uGWoKaslH2DMr0GRpkuLtXvtsP_5JGPVTYxJvuFznF25kKsS")

    server_cmd = "python manage.py runserver 0.0.0.0:8000 > server_log.txt 2>&1"
    threading.Thread(target=lambda: os.system(server_cmd), daemon=True).start()

    public_url = ngrok.connect(8000).public_url
    print(f"🌍 Public URL via ngrok: {public_url}")

    print("📝 Tailing server logs in real-time:\n")
    try:
        stream_logs("server_log.txt")
    except KeyboardInterrupt:
        print("🚫 Log tail stopped.")

if __name__ == "__main__":
    run_server()