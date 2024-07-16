#!/bin/bash

# Update the system and install necessary packages
sudo apt update
sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv git

# Clone the GitHub repository
cd /home/ubuntu/
git clone https://github.com/BravoBravoIX/scse_vm_modules.git

# Navigate to the repository directory
cd scse_vm_modules

# Set up a virtual environment
python3 -m venv myenv

# Activate the virtual environment
source myenv/bin/activate

# Install the required packages
pip install -r requirements.txt

# Create a systemd service for each module to ensure they run after reboots
create_systemd_service() {
  local module_name=$1
  local module_path="/home/ubuntu/scse_vm_modules/$module_name.py"
  local service_file="/etc/systemd/system/$module_name.service"

  sudo bash -c "cat > $service_file" <<EOL
[Unit]
Description=$module_name service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/scse_vm_modules
ExecStart=/home/ubuntu/scse_vm_modules/myenv/bin/python $module_path
Restart=always

[Install]
WantedBy=multi-user.target
EOL

  sudo systemctl daemon-reload
  sudo systemctl enable $module_name.service
  sudo systemctl start $module_name.service
}

# Create systemd services for all modules
create_systemd_service "comm_module"
create_systemd_service "data_module"
create_systemd_service "logging_module"
create_systemd_service "monitoring_module"

echo "Setup complete. Modules are now running and will restart after reboots."

# Deactivate the virtual environment
deactivate
