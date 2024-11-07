# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install required Python packages using the requirements.txt file
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file to the container
COPY .env /app/.env

# Set environment variables (optional, in case the environment variables need defaults)
ENV SENDGRID_API_KEY=""
ENV SENDGRID_SENDER_MAIL=""

# Run the script by default if not overridden
CMD ["python", "./main.py"]
