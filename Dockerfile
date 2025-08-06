# Use a more complete Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Install the necessary libraries for OpenCV and other dependencies
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libfontconfig1

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the command to run the application
CMD gunicorn --bind 0.0.0.0:8000 app:app