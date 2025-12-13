# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt .
# Copy the contents of the src directory into the container at /app
COPY src/ .

# ODBC Dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential \
    curl \
    apt-utils \
    gnupg2 &&\
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip

# Microsoft SQL Server ODBC Driver Installation
RUN curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
RUN curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18


COPY /odbc.ini / 
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run main.py when the container launches
CMD ["python", "main.py"]
