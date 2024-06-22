import os
import time

FILE_PATH = 'simulation.txt'
CONTAINER_NAME = 'knitting-ml'

def read_file_content(file_path):
    with open(file_path, 'r') as f:
        return f.read().strip()

def restart_container(container_name):
    command = f"docker restart {container_name}"
    exit_code = os.system(command)
    if exit_code == 0:
        print(f"Container '{container_name}' restarted successfully.")
    else:
        print(f"Failed to restart container '{container_name}'. Exit code: {exit_code}")

if __name__ == "__main__":
    while True:
        try:
            content = read_file_content(FILE_PATH)
            if content == '1':
                restart_container(CONTAINER_NAME)
            elif content == '0':
                print("File contains '0'. No action taken.")
            else:
                print("Invalid content in file. Expected '0' or '1'.")
            
            time.sleep(5)  # Check every 5 seconds
        except KeyboardInterrupt:
            print("\nStopping the script.")
            break
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)  # Retry after 5 seconds on error
