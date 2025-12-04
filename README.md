📌 Project Title

Flask CRUD API with JSON Storage & Basic Authentication

📖 Description

This is a simple REST API built using Flask that performs basic CRUD operations (Create, Read, Update, Delete) on a local JSON file.
It also uses Basic Authentication for security.

This project is designed as a beginner-friendly backend practice and is ready for future cloud deployment and database integration.

🛠️ Technologies Used

Python

Flask

Flask-HTTPAuth

JSON file storage

Postman (API testing)

Git & GitHub (Version control)

📂 Project Structure
PROJECT/
│
├── app.py
├── data.json
├── README.md
└── venv/

🚀 How to Run the Project
1. Activate the virtual environment

On Windows:

venv\Scripts\activate


On Mac / Linux:

source venv/bin/activate

2. Install required packages
pip install flask flask-httpauth

3. Run the server
python app.py


Server will start at:

http://127.0.0.1:5000

🔐 Authentication (Basic Auth)
Username	Password
admin	password123
user	userpass

Use these in Postman under Authorization → Basic Auth

📡 API Endpoints
✅ GET All Data
GET /api/data

✅ POST Add New Data
POST /api/data


Example Body (JSON):

{
  "name": "John",
  "age": 25
}

✅ PUT Update Data (by index)
PUT /api/data/0

✅ DELETE Data (by index)
DELETE /api/data/0

☁️ Cloud Readiness

Currently data is stored in data.json.

For cloud deployment, this can be easily replaced with:

MongoDB

PostgreSQL

Firebase

Or any cloud database

✅ The system is cloud-ready
✅ Only storage layer needs to be swapped later

🎯 Future Improvements

Add database (MongoDB / PostgreSQL)

Add user registration

Add JWT authentication

Build Frontend (Web / Mobile App)

Deploy to AWS / Render / Railway

👨‍💻 Author

Sivatharshan
Computer Science Graduate | Future Cybersecurity & Software Professional
Currently based in Australia