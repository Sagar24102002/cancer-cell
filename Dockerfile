# Use the official Python image as the base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy requirements.txt first for better Docker layer caching
COPY requirements.txt /app/

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the working directory
COPY . /app

# Expose the port the app runs on
EXPOSE 5000

# Define the entry point for the container
CMD ["python", "app.py"]
