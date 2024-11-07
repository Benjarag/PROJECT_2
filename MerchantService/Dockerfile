# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create a directory for the JSON files
RUN mkdir -p /app/MerchantService

COPY . .

# Expose port for FastAPI
EXPOSE 8001

# Run the app with Uvicorn
CMD ["uvicorn", "application:app", "--host", "0.0.0.0", "--port", "8001"]
