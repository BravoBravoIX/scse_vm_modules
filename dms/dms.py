from flask import Flask, jsonify, request, send_from_directory
import os
import yaml
import subprocess

app = Flask(__name__)
CONFIG_FILE = 'config.yaml'
DATA_DIRS = {}

# Load the configuration file
def load_config():
    with open(CONFIG_FILE, 'r') as file:
        return yaml.safe_load(file)

config = load_config()
controller_ip = config['controller']['ip']
controller_port = config['controller']['port']
base_directory = config['controller']['base_directory']

# Build DATA_DIRS with nested asset directories
for asset in config['assets']:
    asset_id = asset['id']
    DATA_DIRS[asset_id] = {
        'telemetry': os.path.join(base_directory, asset_id, 'telemetry'),
        'images': os.path.join(base_directory, asset_id, 'images')
    }

@app.route('/<asset_id>/<data_type>', methods=['GET'])
def list_data(asset_id, data_type):
    if asset_id not in DATA_DIRS or data_type not in DATA_DIRS[asset_id]:
        return jsonify({"error": "Invalid asset ID or data type"}), 400
    try:
        files = os.listdir(DATA_DIRS[asset_id][data_type])
        return jsonify(files)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/<asset_id>/<data_type>/<filename>', methods=['GET'])
def get_data(asset_id, data_type, filename):
    if asset_id not in DATA_DIRS or data_type not in DATA_DIRS[asset_id]:
        return jsonify({"error": "Invalid asset ID or data type"}), 400
    try:
        return send_from_directory(DATA_DIRS[asset_id][data_type], filename)
    except Exception as e:
        return jsonify({"error": str(e)}), 404

@app.route('/<asset_id>/<data_type>', methods=['POST'])
def receive_data(asset_id, data_type):
    if asset_id not in DATA_DIRS or data_type not in DATA_DIRS[asset_id]:
        return jsonify({"error": "Invalid asset ID or data type"}), 400
    try:
        data = request.json.get('data')
        filename = request.json.get('filename')
        if not data or not filename:
            return jsonify({"error": "Invalid data or filename"}), 400

        file_path = os.path.join(DATA_DIRS[asset_id][data_type], filename)
        with open(file_path, 'w') as file:
            file.write(data)
        return jsonify({"message": "File received"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Start the file moving process as a background process
    subprocess.Popen(['python3', 'move_files.py'])
    
    app.run(host=controller_ip, port=controller_port)
