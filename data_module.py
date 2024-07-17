import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data_dir = '/home/brett/data'  # Path to the data directory
    files = os.listdir(data_dir)
    data = []
    for file in files:
        with open(os.path.join(data_dir, file), 'r') as f:
            data.append(f.read())
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
