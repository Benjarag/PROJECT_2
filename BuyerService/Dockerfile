# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8002 for the FastAPI app
EXPOSE 8002

# Start the FastAPI app with uvicorn on port 8002
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8002"]

# # Base image
# FROM python:3.11-slim

# # Set working directory
# WORKDIR /app

# # Copy project files
# COPY requirements.txt requirements.txt

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# # Expose port for FastAPI
# EXPOSE 8002

# # Run the app with Uvicorn
# CMD ["uvicorn", "app:main", "--host", "0.0.0.0", "--port", "8002"]
