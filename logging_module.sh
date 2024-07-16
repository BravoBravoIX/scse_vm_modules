#!/bin/bash

# Logging Module Script
# This script sets up logging for the VM, ensuring all relevant events and statuses are recorded.

# Constants
LOG_DIR="/var/log/space_cyber_range"
LOG_FILE="$LOG_DIR/system.log"

# Create the log directory if it doesn't exist
mkdir -p $LOG_DIR

# Function to log messages
log_message() {
    local log_level=$1
    local log_message=$2
    echo "$(date '+%Y-%m-%d %H:%M:%S') [$log_level] $log_message" >> $LOG_FILE
}

# Log the start of the logging module setup
log_message "INFO" "Starting logging module setup."

# Install necessary packages
apt-get update
apt-get install -y rsyslog

# Configure rsyslog to log to our custom log file
echo "Creating rsyslog configuration for custom logging..."
cat <<EOF > /etc/rsyslog.d/space_cyber_range.conf
# Custom logging for Space Cyber Range
module(load="imuxsock")
module(load="imklog")

$FileOwner root
$FileGroup adm
$FileCreateMode 0640
$DirCreateMode 0755
$Umask 0022

# Log all messages to our custom log file
*.* $LOG_FILE
EOF

# Restart rsyslog to apply changes
systemctl restart rsyslog

# Log the completion of the logging module setup
log_message "INFO" "Logging module setup complete."

# Commented section: Interactions with the control server

# The logging module interacts with the control server by sending logs via HTTP POST requests.
# It reports critical events and statuses as defined in the configuration.
# Example interactions:
# - When a new data file is received: log_message "INFO" "Received new data file: $file_name"
# - When a command is executed: log_message "INFO" "Executed command: $command"

# To run this script automatically on VM startup, you can use cloud-init or systemd services.
# Example cloud-init configuration:
# runcmd:
#   - /path/to/logging_module.sh

# The expected outcome of running this script:
# - The log directory /var/log/space_cyber_range is created.
# - The system log file /var/log/space_cyber_range/system.log is created and populated with log entries.
# - rsyslog is configured to log all messages to the custom log file.
# - Log entries are written to the log file whenever the log_message function is called.
