from flask import Flask, request, jsonify
import aerospike
import os

app = Flask(__name__)

# Aerospike config
config = {
    'hosts': [(os.getenv('AEROSPIKE_HOST', '127.0.0.1'), 3000)]
}

# Global client variable
client = None

# Connect to Aerospike
try:
    client = aerospike.client(config).connect()
except Exception as e:
    print("Aerospike connection error:", e)


@app.route('/')
def index():
    if client:
        return "Test App Connected to Aerospike!"
    else:
        return "Aerospike not connected!", 500


@app.route('/write', methods=['POST'])
def write():
    if client is None:
        return jsonify({"error": "Aerospike client not connected"}), 500

    body = request.get_json()
    if not body or 'key' not in body or 'value' not in body:
        return jsonify({"error": "Missing key or value"}), 400

    key = ('test', 'demo-set', body['key'])
    try:
        client.put(key, {"value": body['value']})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/read/<key_id>', methods=['GET'])
def read(key_id):
    if client is None:
        return jsonify({"error": "Aerospike client not connected"}), 500

    key = ('test', 'demo-set', key_id)
    try:
        (key, meta, bins) = client.get(key)
        return jsonify(bins), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
