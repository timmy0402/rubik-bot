# Stage 1: Builder
# Used to compile dependencies and install build tools
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
# unixodbc-dev is required for pyodbc compilation
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg2 \
    unixodbc-dev \
    apt-utils

# Install Python dependencies to a specific prefix for easy copying
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --prefix=/install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
# Minimal image for production
FROM python:3.11-slim

WORKDIR /app

# Install only runtime dependencies
# msodbcsql18 requires curl/gnupg for repo setup, but we clean up apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    env ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    # Cleanup to keep layer size down
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy installed python dependencies from builder
COPY --from=builder /install /usr/local

# Copy ODBC configuration
COPY odbc.ini /
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini

# Copy application code
COPY src/ .

CMD ["python", "main.py"]
