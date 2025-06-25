# Use an official Python image
FROM python:3.12-slim

# Install system dependencies for pyodbc
RUN apt-get update && \
    apt-get install -y gcc g++ unixodbc-dev && \
    rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Expose the port Railway expects
EXPOSE 8080

# Start the app with gunicorn from the current directory
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
