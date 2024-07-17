import os
import time
import yaml
import shutil

CONFIG_FILE = 'config.yaml'

def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)

def move_files():
    config = load_config()
    while True:
        for asset in config['assets']:
            asset_id = asset['id']
            base_dir = config['controller']['base_directory']
            for data_type in asset['data_types']:
                name = data_type['name']
                frequency = data_type['frequency']
                source_dir = os.path.join(base_dir, asset_id, f"{name}_unsent")
                target_dir = os.path.join(base_dir, asset_id, name)

                # Check if source directory exists
                if not os.path.exists(source_dir):
                    continue

                # Get the list of files in the source directory, sorted by name
                files = sorted(os.listdir(source_dir))
                if files:
                    file_to_move = files[0]
                    source_path = os.path.join(source_dir, file_to_move)
                    target_path = os.path.join(target_dir, file_to_move)
                    
                    # Move the file and delete from the source directory
                    shutil.move(source_path, target_path)

                # Wait for the specified frequency before moving the next file
                time.sleep(frequency)

if __name__ == "__main__":
    move_files()
