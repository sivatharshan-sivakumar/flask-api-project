 Project Evolution / Version History

This project was developed in multiple phases to demonstrate real-world backend progression — starting from a simple local API and gradually transforming into a cloud-ready, Dockerized, multi-format backend system.

🔹 Phase 1 — Basic Local CRUD API (Initial Version)

Features implemented:

Flask server with /api/data route

JSON-only request & response

Local storage in data.json

Basic Create, Read, Update, Delete

Tested with Postman

Purpose:
Build a simple working REST API — ideal as a beginner backend foundation.

🔹 Phase 2 — Authentication Added

Upgrades:

Integrated Basic Authentication (Flask-HTTPAuth)

Passwords hashed using Werkzeug

Postman authentication testing

Purpose:
Introduce API security and authenticated access.

🔹 Phase 3 — XML Support Added

Major enhancements:

API can accept XML input

API can return XML output

Automatic format detection:

Based on Content-Type and Accept headers

XML parsing using xmltodict

Clean XML formatting using dicttoxml

Purpose:
Support both JSON and XML clients — useful for IoT, legacy systems, and enterprise integrations.

🔹 Phase 4 — Input Validation Layer

Upgrades:

Gateway/device payload validation

Ensured:

gatewayID required

devices required

Each device must have name + voltage

Rejects invalid XML or JSON

Purpose:
Prevent malformed or unexpected payloads — required for real APIs.

🔹 Phase 5 — Migrated Storage from JSON → AWS DynamoDB

Upgrades:

Connected AWS DynamoDB using boto3

Created DynamoDB table Gateways

Replaced file operations with:

scan()

put_item()

get_item()

delete_item()

Supports cloud-based persistent storage

Purpose:
Make the system cloud-ready and scalable.

🔹 Phase 6 — Dockerized the Application

Enhancements:

Added Dockerfile

Packaged Flask API + all dependencies

Set environment variables for AWS credentials

Tested container with:

docker build -t flask-api .
docker run -p 5000:5000 flask-api


Purpose:
Ensure your API runs consistently across all machines and is ready for deployment.

🔹 Phase 7 — Cloud Deployment Ready

(Not fully deployed yet, but structure prepared)

Prepared for:

AWS EC2 deployment

HTTPS via AWS Load Balancer

GitHub CI/CD

Scaling with ECS or Kubernetes

Purpose:
Next step toward real-world production hosting.