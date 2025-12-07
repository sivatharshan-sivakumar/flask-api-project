import boto3
import json
from flask import Flask, jsonify, request, Response
from flask_httpauth import HTTPBasicAuth
import xmltodict
from dicttoxml import dicttoxml
from werkzeug.security import generate_password_hash, check_password_hash

# ============================================================
# AWS DYNAMODB SETUP
# ============================================================
# Connect to DynamoDB (Sydney Region)
dynamodb = boto3.resource("dynamodb", region_name="ap-southeast-2")

# Use your table "Gateways"
table = dynamodb.Table("Gateways")

# ============================================================
# FLASK + AUTHENTICATION SETUP
# ============================================================
app = Flask(__name__)
auth = HTTPBasicAuth()

# Limit payload sizes for security (1MB)
app.config["MAX_CONTENT_LENGTH"] = 1 * 1024 * 1024

# Passwords are stored as HASHES (NEVER plain text)
users = {
    "admin": generate_password_hash("password123"),
    "user": generate_password_hash("userpass")
}

@auth.verify_password
def verify(username, password):
    if username in users and check_password_hash(users[username], password):
        return username
    return None


# ============================================================
# VALIDATION FOR GATEWAY + DEVICE STRUCTURE
# ============================================================
def validate_gateway_payload(payload):
    """
    Ensures payload contains:
    - gatewayID (string)
    - devices (list)
    - each device has name + voltage
    """
    if not isinstance(payload, dict):
        return False, "Payload must be an object"

    if "gatewayID" not in payload:
        return False, "Missing gatewayID"

    if "devices" not in payload:
        return False, "Missing devices"

    devices = payload["devices"]

    # Normalize XML wrapping
    if isinstance(devices, dict) and "device" in devices:
        devices = devices["device"]

    if not isinstance(devices, list):
        devices = [devices]

    for i, d in enumerate(devices):
        if "name" not in d:
            return False, f"Device #{i} missing name"
        if "voltage" not in d:
            return False, f"Device #{i} missing voltage"

    return True, None


# ============================================================
# XML HELPERS
# ============================================================
def is_xml_request():
    return request.content_type == "application/xml"

def clean_xml(data):
    """Formats DynamoDB data into clean XML output."""
    if isinstance(data, list):
        return {"gateways": {"gateway": [clean_xml(i) for i in data]}}

    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if isinstance(v, list):
                cleaned[k] = {"device": [clean_xml(d) for d in v]}
            else:
                cleaned[k] = v
        return cleaned

    return data

def xml_response(data):
    cleaned = clean_xml(data)
    xml_bytes = dicttoxml(cleaned, custom_root="response", attr_type=False)
    return Response(xml_bytes, mimetype="application/xml")


# ============================================================
# GET ALL GATEWAYS
# ============================================================
@app.route("/api/data", methods=["GET"])
@auth.login_required
def get_all():
    """Retrieve ALL gateway records from DynamoDB."""
    response = table.scan()
    items = response.get("Items", [])

    if "application/xml" in request.headers.get("Accept", ""):
        return xml_response(items)

    return jsonify(items)


# ============================================================
# GET A SINGLE GATEWAY BY ID
# ============================================================
@app.route("/api/data/<gatewayID>", methods=["GET"])
@auth.login_required
def get_one(gatewayID):
    """Retrieve one gateway record by its ID."""
    response = table.get_item(Key={"gatewayID": gatewayID})

    if "Item" not in response:
        return jsonify({"error": "Gateway not found"}), 404

    item = response["Item"]

    if "application/xml" in request.headers.get("Accept", ""):
        return xml_response(item)

    return jsonify(item)


# ============================================================
# CREATE A NEW GATEWAY
# ============================================================
@app.route("/api/data", methods=["POST"])
@auth.login_required
def add_gateway():
    """Add a new gateway to DynamoDB."""

    # Parse XML or JSON
    if is_xml_request():
        parsed = xmltodict.parse(request.data)
        payload = parsed.get("item") or parsed
    else:
        payload = request.get_json()

    # Validate
    valid, msg = validate_gateway_payload(payload)
    if not valid:
        return jsonify({"error": msg}), 400

    # Save to DynamoDB
    table.put_item(Item=payload)

    # Response
    if is_xml_request():
        return xml_response({"message": "Gateway added", "data": payload}), 201

    return jsonify({"message": "Gateway added", "data": payload}), 201


# ============================================================
# UPDATE A GATEWAY
# ============================================================
@app.route("/api/data/<gatewayID>", methods=["PUT"])
@auth.login_required
def update_gateway(gatewayID):
    """Update a gateway by ID."""

    if is_xml_request():
        parsed = xmltodict.parse(request.data)
        payload = parsed.get("item") or parsed
    else:
        payload = request.get_json()

    valid, msg = validate_gateway_payload(payload)
    if not valid:
        return jsonify({"error": msg}), 400

    # Force the URL ID to be the actual item key
    payload["gatewayID"] = gatewayID

    table.put_item(Item=payload)

    if is_xml_request():
        return xml_response({"message": "Gateway updated", "data": payload})

    return jsonify({"message": "Gateway updated", "data": payload})


# ============================================================
# DELETE A GATEWAY
# ============================================================
@app.route("/api/data/<gatewayID>", methods=["DELETE"])
@auth.login_required
def delete_gateway(gatewayID):
    """Delete a gateway by ID."""
    table.delete_item(Key={"gatewayID": gatewayID})

    if is_xml_request():
        return xml_response({"message": "Gateway deleted"})

    return jsonify({"message": "Gateway deleted"})


# ============================================================
# GENERIC 500 ERROR HANDLER
# ============================================================
@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


# ============================================================
# START FLASK SERVER
# ============================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

