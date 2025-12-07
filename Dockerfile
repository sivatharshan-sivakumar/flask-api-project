# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements file first (helps caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all remaining files
COPY . .

# Expose Flask port
EXPOSE 5000

# --- DO NOT put credentials here ---
# We leave AWS vars empty so Dockerfile stays safe
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV AWS_DEFAULT_REGION="ap-southeast-2"

# Start Flask app
CMD ["python", "app.py"]
