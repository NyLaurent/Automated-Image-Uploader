import os
import time
import subprocess
from shutil import move

MONITOR_DIR = r"C:\Users\user\Downloads\test5"
UPLOADED_DIR = os.path.join(MONITOR_DIR, "uploaded")
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

os.makedirs(os.path.normpath(UPLOADED_DIR), exist_ok=True)

def upload_file(file_path):
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL],
            capture_output=True,
            text=True
        )
        if result.returncode == 0 and "200" in result.stdout:
            print(f"Upload successful: {file_path}")
            return True
        else:
            print(f"Upload failed for {file_path}: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error during upload: {e}")
        return False

def monitor_folder():
    print(f"Monitoring folder: {MONITOR_DIR}")
    while True:
        files = [f for f in os.listdir(MONITOR_DIR) if os.path.isfile(os.path.join(MONITOR_DIR, f))]
        for file_name in files:
            file_path = os.path.join(MONITOR_DIR, file_name)
            if time.time() - os.path.getmtime(file_path) >= 30:  
                if upload_file(file_path):
                    move(file_path, os.path.join(UPLOADED_DIR, file_name))
        time.sleep(10)

if __name__ == "__main__":
    monitor_folder()