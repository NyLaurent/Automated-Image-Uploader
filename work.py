import os
import time
import subprocess
import shutil

# Define the folder where pictures are saved
camera_folder = r"C:\Users\user\Downloads\test5"

# Define the folder where uploaded pictures will be moved
uploaded_folder = r"C:\Users\user\Downloads\test4"

# Ensure the uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)

# Function to upload the file using `curl` command
def upload_file(file_path):
    try:
        # Construct the `curl` command
        url = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"
        command = [
            "curl",
            "-X", "POST",
            "-F", f"imageFile=@{file_path}",
            url
        ]
        
        # Run the `curl` command
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Check if the upload was successful
        if result.returncode == 0:
            print(f"{file_path} uploaded successfully!")
            print(f"Response: {result.stdout.strip()}")
            return True
        else:
            print(f"Failed to upload {file_path}. Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"Error during upload of {file_path}: {e}")
        return False

def monitor_and_upload():
    while True:
        try:
            # List all files in the folder
            files = os.listdir(camera_folder)
            files = [f for f in files if os.path.isfile(os.path.join(camera_folder, f))]

            for file_name in files:
                file_path = os.path.join(camera_folder, file_name)

                # Wait 30 seconds before attempting upload
                print(f"Waiting 30 seconds to upload: {file_name}")
                time.sleep(30)

                # Upload the file
                if upload_file(file_path):
                    # Move the file to the uploaded folder after a successful upload
                    destination_path = os.path.join(uploaded_folder, file_name)
                    shutil.move(file_path, destination_path)
                    print(f"{file_name} moved to {uploaded_folder} after upload.")

        except Exception as e:
            print(f"Error: {e}")
        finally:
            # Wait before checking for new files again
            time.sleep(5)

if __name__ == "__main__":
    monitor_and_upload()