import json
from flask import Flask, jsonify, request
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

# Simple user store (username: password)
users = {"admin": "password123", "user": "userpass"}

@auth.verify_password
def verify(username, password):
    if username in users and users[username] == password:
        return username
    return None

DATA_FILE = 'data.json'

# Helper functions to read/write JSON
def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# GET data
@app.route('/api/data', methods=['GET'])
@auth.login_required
def get_data():
    return jsonify(read_data())

# POST new data
@app.route('/api/data', methods=['POST'])
@auth.login_required
def add_data():
    new_item = request.get_json()
    data = read_data()
    data.append(new_item)
    write_data(data)
    return jsonify({"message": "Item added", "data": new_item}), 201

# PUT update data by index
@app.route('/api/data/<int:item_id>', methods=['PUT'])
@auth.login_required
def update_data(item_id):
    data = read_data()
    if 0 <= item_id < len(data):
        updated_item = request.get_json()
        data[item_id] = updated_item
        write_data(data)
        return jsonify({"message": "Item updated", "data": updated_item})
    return jsonify({"error": "Item not found"}), 404

# DELETE data by index
@app.route('/api/data/<int:item_id>', methods=['DELETE'])
@auth.login_required
def delete_data(item_id):
    data = read_data()
    if 0 <= item_id < len(data):
        removed_item = data.pop(item_id)
        write_data(data)
        return jsonify({"message": "Item deleted", "data": removed_item})
    return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
