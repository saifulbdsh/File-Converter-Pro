# Use a complete Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the command to run the application
CMD gunicorn --bind 0.0.0.0:8000 app:app