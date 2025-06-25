from flask import Flask, request, jsonify
import aerospike
import os

config = {
    'hosts': [(os.getenv('AEROSPIKE_HOST', '127.0.0.1'), 3000)]
}

app = Flask(__name__)

try:
    client = aerospike.client(config).connect()
except Exception as e:
    print("Aerospike connection error:", e)

@app.route('/')
def index():
    return "Test App Connected to Aerospike!"

@app.route('/write', methods=['POST'])
def write():
    body = request.get_json()
    key = ('test', 'demo-set', body['key'])
    try:
        client.put(key, {"value": body['value']})
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read/<key_id>', methods=['GET'])
def read(key_id):
    key = ('test', 'demo-set', key_id)
    try:
        (key, meta, bins) = client.get(key)
        return jsonify(bins), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
