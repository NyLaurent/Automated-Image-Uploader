# Import required libraries
import os              # For file and directory operations
import time           # For time-related functions
import subprocess     # For running external commands (curl)
from shutil import move  # For moving files between directories

# Define constants
MONITOR_DIR = r"C:\Users\user\Downloads\test5"  # Directory to monitor for new files
UPLOADED_DIR = os.path.join(MONITOR_DIR, "uploaded")  # Subdirectory for successfully uploaded files
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"  # Target URL for file uploads

# Create the uploaded directory if it doesn't exist
os.makedirs(os.path.normpath(UPLOADED_DIR), exist_ok=True)

def upload_file(file_path):
    
    try:
        # Execute curl command to upload the file
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", UPLOAD_URL],
            capture_output=True,
            text=True
        )
        # Check if upload was successful (return code 0 and "200" in response)
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
        # Get list of all files (not directories) in the monitored folder
        files = [f for f in os.listdir(MONITOR_DIR) if os.path.isfile(os.path.join(MONITOR_DIR, f))]
        
        for file_name in files:
            file_path = os.path.join(MONITOR_DIR, file_name)
            # Check if file hasn't been modified in the last 30 seconds
            if time.time() - os.path.getmtime(file_path) >= 30:  
                # Try to upload the file
                if upload_file(file_path):
                    # If upload successful, move file to uploaded directory
                    move(file_path, os.path.join(UPLOADED_DIR, file_name))
        
        # Wait for 10 seconds before checking again
        time.sleep(10)

# Entry point of the script
if __name__ == "__main__":
    monitor_folder()