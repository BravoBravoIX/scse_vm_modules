import requests
import logging

# Setup logging
logging.basicConfig(filename='data_module.log', level=logging.INFO, 
                    format='%(asctime)s %(levelname)s %(message)s')

class DataModule:
    def __init__(self, dms_url, storage_path):
        self.dms_url = dms_url
        self.storage_path = storage_path
        logging.info(f"Data Module initialized with DMS URL: {dms_url} and storage path: {storage_path}")

    def ingest_data(self):
        """
        Fetch data from the DMS and store it locally.
        """
        try:
            response = requests.get(f"{self.dms_url}/data")
            response.raise_for_status()
            data = response.json()
            with open(self.storage_path, 'w') as file:
                file.write(data)
            logging.info("Data ingested and stored successfully.")
        except Exception as e:
            logging.error(f"Failed to ingest data: {e}")

    def retrieve_data(self):
        """
        Read and return data stored locally.
        """
        try:
            with open(self.storage_path, 'r') as file:
                data = file.read()
            logging.info("Data retrieved successfully.")
            return data
        except Exception as e:
            logging.error(f"Failed to retrieve data: {e}")

    def push_data(self, data):
        """
        Send generated data to the DMS.
        """
        try:
            response = requests.post(f"{self.dms_url}/data", json=data)
            response.raise_for_status()
            logging.info("Data pushed to DMS successfully.")
        except Exception as e:
            logging.error(f"Failed to push data: {e}")

if __name__ == "__main__":
    # Example usage
    data_module = DataModule(dms_url="http://192.168.1.1:5000", storage_path="/home/ubuntu/data.txt")
    data_module.ingest_data()
    local_data = data_module.retrieve_data()
    print(f"Retrieved data: {local_data}")
    data_module.push_data({"example_key": "example_value"})
