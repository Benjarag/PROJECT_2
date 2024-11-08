# Use the official Python image as a base
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8002 for the FastAPI app
EXPOSE 8000
# Start the FastAPI app with uvicorn on port 8002
CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8000"]
