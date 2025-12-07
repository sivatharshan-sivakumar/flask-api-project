Flask IoT Gateway API — JSON, XML, DynamoDB, Authentication, Dockerized

This project demonstrates a real-world backend progression, starting from a simple CRUD API and evolving into a cloud-ready, multi-format, secure, and containerized service.

 Project Evolution / Version History
🔹 Phase 1 — Basic Local CRUD API (Initial Version)

Features implemented:

Flask server with /api/data

JSON-only request & response

Local data storage in data.json

CRUD operations: GET, POST, PUT, DELETE

API tested using Postman

Purpose:
Build a simple working REST API — a solid beginner backend foundation.

🔹 Phase 2 — Added Authentication

Upgrades:

Integrated Flask-HTTPAuth

Implemented Basic Authentication

Passwords stored using hashing (Werkzeug)

Verified via Postman

Purpose:
Introduce security and restricted access to API endpoints.

🔹 Phase 3 — Added XML Support

Enhancements:

API accepts XML input

API returns XML output

Format auto-detected via headers:

Content-Type

Accept

XML parsing using xmltodict

Clean XML output using dicttoxml

Purpose:
Enable support for IoT devices, enterprise systems, and legacy clients that require XML.

🔹 Phase 4 — Input Validation Layer

Implemented validation rules:

gatewayID required

devices required

Each device requires:

name

voltage

Rejects malformed XML/JSON.

Purpose:
Ensure reliability and prevent corrupted data.

🔹 Phase 5 — Migration to AWS DynamoDB

Upgrades:

Integrated boto3 SDK

Replaced JSON file operations with DynamoDB:

scan()

put_item()

get_item()

delete_item()

All gateway entries now stored in AWS.

Purpose:
Make the system scalable and cloud-ready.

🔹 Phase 6 — Dockerization

Enhancements:

Added Dockerfile

Packaged Flask API into a Docker image

Injected AWS credentials via environment variables

Tested with:

docker build -t flask-api .
docker run -p 5000:5000 flask-api


Purpose:
Ensure the API runs the same everywhere — local or cloud.

🔹 Phase 7 — AWS Deployment Ready

(Prepared but not deployed yet)

Supports:

Deployment to AWS EC2

HTTPS using AWS Load Balancer

CI/CD with GitHub Actions

Future scaling via ECS or Kubernetes

Purpose:
Move toward production-grade hosting.

Technologies Used

Python

Flask

Flask-HTTPAuth

DynamoDB (AWS)

JSON & XML processing

Docker

Postman

Git & GitHub

 Project Structure
PROJECT/
│── app.py
│── Dockerfile
│── requirements.txt
│── data.json (legacy local storage)
│── README.md
└── venv/

 Authentication

Use Basic Auth in Postman:

Username	Password
admin	password123
user	userpass
📡 API Endpoints
GET all gateways
GET /api/data

GET a single gateway
GET /api/data/<gatewayID>

POST add a gateway
POST /api/data

PUT update a gateway
PUT /api/data/<gatewayID>

DELETE a gateway
DELETE /api/data/<gatewayID>


Supports both JSON and XML input/output.

 Docker Commands

Build:

docker build -t flask-api .


Run:

docker run -p 5000:5000 flask-api


Stop (if running):

docker ps
docker stop <container_id>

 Cloud Readiness

The system is now:

Scalable

Portable

Compatible with AWS services

Ready for EC2 hosting

Ready for HTTPS termination

👨‍💻 Author

Sivatharshan
Computer Science Graduate | Future Software Engineer
Currently based in Australia