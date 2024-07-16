#!/bin/bash

# Monitoring Module Script
# This script sets up monitoring for the VM, ensuring system health and performance metrics are tracked.

# Constants
MONITOR_DIR="/var/monitor/space_cyber_range"
MONITOR_LOG="$MONITOR_DIR/monitor.log"

# Create the monitoring directory if it doesn't exist
mkdir -p $MONITOR_DIR

# Function to log monitoring data
monitor_log() {
    local monitor_message=$1
    echo "$(date '+%Y-%m-%d %H:%M:%S') $monitor_message" >> $MONITOR_LOG
}

# Log the start of the monitoring module setup
monitor_log "Starting monitoring module setup."

# Install necessary packages
apt-get update
apt-get install -y sysstat

# Function to monitor CPU usage
monitor_cpu() {
    while true; do
        local cpu_usage=$(mpstat | awk '$12 ~ /[0-9.]+/ { print 100 - $12 }')
        monitor_log "CPU Usage: $cpu_usage%"
        sleep 10  # Adjust the frequency as needed
    done
}

# Function to monitor memory usage
monitor_memory() {
    while true; do
        local memory_usage=$(free | awk '/Mem/ { printf("%.2f"), $3/$2*100 }')
        monitor_log "Memory Usage: $memory_usage%"
        sleep 10  # Adjust the frequency as needed
    done
}

# Start monitoring in the background
monitor_cpu &
monitor_memory &

# Log the completion of the monitoring module setup
monitor_log "Monitoring module setup complete."

# Commented section: Interactions with the control server

# The monitoring module interacts with the control server by sending system health and performance metrics via HTTP POST requests.
# Example interactions:
# - Periodic CPU usage: monitor_log "CPU Usage: $cpu_usage%"
# - Periodic memory usage: monitor_log "Memory Usage: $memory_usage%"

# To run this script automatically on VM startup, you can use cloud-init or systemd services.
# Example cloud-init configuration:
# runcmd:
#   - /path/to/monitoring_module.sh

# The expected outcome of running this script:
# - The monitor directory /var/monitor/space_cyber_range is created.
# - The monitoring log file /var/monitor/space_cyber_range/monitor.log is created and populated with monitoring data.
# - CPU and memory usage are logged periodically.
