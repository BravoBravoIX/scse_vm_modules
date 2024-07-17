import os
import requests
import time
import yaml
import logging
import socket

class DataModule:
    def __init__(self, config_file='config.yaml'):
        self.config = self.load_config(config_file)
        self.current_ip = self.get_current_ip()
        logging.info(f'Current IP: {self.current_ip}')
        self.satellite = self.get_current_satellite()
        self.setup_logging()
        self.create_directories()

    def setup_logging(self):
        log_file = os.path.expanduser(self.satellite['logging']['log_file'])
        log_dir = os.path.dirname(log_file)
        os.makedirs(log_dir, exist_ok=True)

        logging.basicConfig(filename=log_file, level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')
        logging.info('Logging setup complete')

    def load_config(self, config_file):
        with open(config_file, 'r') as file:
            config = yaml.safe_load(file)
        logging.info(f"Configuration loaded: {config}")
        return config

    def get_current_satellite(self):
        for satellite in self.config.get('assets', []):
            logging.info(f"Checking satellite: {satellite}")
            if satellite['ip'] == self.current_ip:
                return satellite
        raise ValueError("Current satellite configuration not found")

    def get_current_ip(self):
        try:
            # Connect to a public IP address (Google DNS)
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logging.error(f"Error getting current IP: {e}")
            return "127.0.0.1"

    def create_directories(self):
        base_dir = self.satellite['base_directory']
        directories = []
        directories.extend(self.satellite['retrieval_directories'].values())
        directories.extend(self.satellite['sending_directories'].values())
        for directory in directories:
            full_path = os.path.join(base_dir, directory)
            os.makedirs(os.path.expanduser(full_path), exist_ok=True)
        logging.info('Directories created or already exist')

    def retrieve_data(self):
        asset_id = self.satellite['id']
        for data_type in self.satellite['data_types']:
            directory = os.path.join(self.satellite['base_directory'], self.satellite['retrieval_directories'].get(data_type['name']))
            if directory:
                try:
                    url = f"http://{self.config['controller']['ip']}:{self.config['controller']['port']}/{asset_id}/{data_type['name']}"
                    logging.info(f"Requesting data listing from {url}")
                    response = requests.get(url)
                    logging.info(f"Received response: {response.status_code}")
                    if response.status_code == 200:
                        files = response.json()
                        logging.info(f"Files received: {files}")
                        for file in files:
                            self.retrieve_file_if_not_exists(url, directory, file)
                    else:
                        logging.error(f"Failed to retrieve data listing from controller: {response.status_code}")
                except Exception as e:
                    logging.error(f"Error retrieving data from controller: {e}")

    def retrieve_file_if_not_exists(self, url, directory, filename):
        filepath = os.path.join(directory, filename)
        if not os.path.exists(filepath):
            self.retrieve_file(url, directory, filename)
        else:
            logging.info(f"File {filename} already exists at {filepath}")

    def retrieve_file(self, url, directory, filename):
        try:
            file_url = f"{url}/{filename}"
            logging.info(f"Requesting file {file_url}")
            response = requests.get(file_url)
            logging.info(f"Received response: {response.status_code}")
            if response.status_code == 200:
                data = response.content
                self.save_data(directory, filename, data)
            else:
                logging.error(f"Failed to retrieve file {filename}: {response.status_code}")
        except Exception as e:
            logging.error(f"Error retrieving file {filename}: {e}")

    def save_data(self, directory, filename, data):
        os.makedirs(directory, exist_ok=True)
        filepath = os.path.join(directory, filename)
        with open(filepath, 'wb') as file:
            file.write(data)
        logging.info(f"Data saved to {filepath}")

    def run(self):
        while True:
            self.retrieve_data()
            time.sleep(20)  # This can be adjusted per data type if needed

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    data_module = DataModule(config_file='config.yaml')
    data_module.run()
