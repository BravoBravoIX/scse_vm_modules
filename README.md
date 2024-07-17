# SCSE VM Modules

This repository contains modules for managing and simulating data transfer between a Data Management System (DMS), satellite, and ground station in a cyber range environment. The modules include data retrieval, communication, and directory setup scripts.

## Setup

### Prerequisites

- Python 3.x
- Flask
- PyYAML

### Installation

1. Clone the repository and navigate to the directory.
2. Create a virtual environment and install dependencies.
3. Set up the directory structure and create sample files using the provided bash script.

### Configuration

Ensure the `config.yaml` file is correctly set up with the necessary IP addresses, ports, and directory paths.

## Modules

### DMS Module (dms.py)

This module serves as the Data Management System (DMS) that provides data to the satellite and ground station VMs. It handles requests for data listings and specific files and receives data from assets.

### Data Module (data_module.py)

This module handles data retrieval from the DMS and saves it to the appropriate directories on the satellite and ground station VMs. It periodically requests data listings from the DMS and retrieves new files that are not already present locally.

### Communication Module (comm_module.py)

This module handles data communication between the satellite/ground station and the DMS. It monitors directories for new data and sends this data to the DMS when it appears.

### File Distribution Module (file_distribution.py)

This module moves files from "unsent" directories to the main directories based on specified frequencies. It simulates the process of a satellite taking images or collecting telemetry data by periodically moving files according to the configuration in `config.yaml`.

### Setup Asset Script (setup_asset.sh)

This bash script sets up the necessary directory structure and sample files for each asset. It prompts for the instance ID and asset ID, creates directories, and populates them with sample files.



## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For any questions or suggestions, please contact brett@cyberops.com.au

---

Thank you for using the SCSE VM Modules!
