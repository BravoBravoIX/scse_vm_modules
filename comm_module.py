import yaml
import logging
import time
import requests

class CommModule:
    def __init__(self):
        """
        Initialize the communication module with the configuration file.
        """
        self.config = self.load_config()
        self.satellite_config = self.config.get('satellite_config')
        self.data_sources = self.config.get('data_sources')
        self.setup_logging()

    def load_config(self):
        """
        Load the configuration from the config.yaml file.
        """
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)

    def setup_logging(self):
        """
        Set up logging configuration.
        """
        logging.basicConfig(filename='comm_module.log', level=logging.INFO,
                            format='%(asctime)s %(levelname)s %(message)s')

    def run(self):
        """
        Main loop to manage communication based on configuration.
        """
        if not self.data_sources:
            logging.error('No data sources found in configuration')
            return

        while True:
            for source in self.data_sources:
                try:
                    if source['type'] == 'pull':
                        response = requests.get(f"http://{source['ip']}:{source['port']}/data")
                        if response.status_code == 200:
                            logging.info(f"Data retrieved from {source['name']}: {response.json()}")
                        else:
                            logging.error(f"Failed to retrieve data from {source['name']}: {response.status_code}")
                except Exception as e:
                    logging.error(f"Failed to retrieve data from {source['name']}: {e}")
                time.sleep(source['frequency'])

if __name__ == "__main__":
    comm_module = CommModule()
    comm_module.run()
