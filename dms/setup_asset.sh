#!/bin/bash

echo "Enter instance ID (e.g., instance_123):"
read instance_id

echo "Enter asset ID (1 or 2):"
read asset_id

base_directory="/home/dms/$instance_id"

# Directories to be created
directories=(
    "$base_directory/asset_$asset_id/telemetry_unsent"
    "$base_directory/asset_$asset_id/images_unsent"
    "$base_directory/asset_$asset_id/telemetry"
    "$base_directory/asset_$asset_id/images"
)

# Create instance ID directory
mkdir -p "$base_directory"
if [ $? -eq 0 ]; then
    echo "Instance directory $base_directory created successfully."
else
    echo "Failed to create instance directory $base_directory."
    exit 1
fi

# Create directories
for dir in "${directories[@]}"; do
    mkdir -p "$dir"
    if [ $? -eq 0 ]; then
        echo "Directory $dir created successfully."
    else
        echo "Failed to create directory $dir."
    fi
done

echo "Directories created successfully."

# Function to create sample files
create_sample_files() {
    local dir=$1
    local extension=$2
    for i in {1..6}; do
        touch "$dir/${i}_sample.$extension"
        if [ $? -eq 0 ]; then
            echo "Created file $dir/${i}_sample.$extension."
        else
            echo "Failed to create file $dir/${i}_sample.$extension."
        fi
    done
}

# Create sample files
create_sample_files "$base_directory/asset_$asset_id/telemetry_unsent" "txt"
create_sample_files "$base_directory/asset_$asset_id/images_unsent" "jpg"

echo "Sample files created successfully."
