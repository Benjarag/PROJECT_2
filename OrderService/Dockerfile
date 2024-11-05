# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose port for FastAPI
EXPOSE 8000

# Run the app with Uvicorn
CMD ["uvicorn", "endpoints:app", "--host", "0.0.0.0", "--port", "8000"]
