# Use a base Python image
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Install the necessary library for OpenCV
RUN apt-get update && apt-get install -y libgl1-mesa-glx

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the command to run the application
CMD gunicorn --bind 0.0.0.0:8000 app:app