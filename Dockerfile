# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# Copy the contents of the src directory into the container at /app
COPY src/ .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Clean up and update package lists, then install Node.js
RUN apt-get clean && apt-get update && apt-get install -y --fix-missing nodejs npm

# Run main.py when the container launches
CMD ["python", "main.py"]
