# Stage 1: Builder
# Used to compile dependencies and install build tools
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
# unixodbc-dev is required for pyodbc compilation
# libcairo2-dev and pkg-config are required for pycairo
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gnupg2 \
    unixodbc-dev \
    pkg-config \
    libcairo2-dev \
    apt-utils

# Create virtual environment efficiently
RUN python -m venv /opt/venv
# Enable venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Stage 2: Runtime
# Minimal image for production
FROM python:3.11-slim AS runtime

WORKDIR /app

# Install only runtime dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl \
    gnupg2 \
    unixodbc \
    libcairo2 && \
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg && \
    curl https://packages.microsoft.com/config/debian/12/prod.list | tee /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    env ACCEPT_EULA=Y apt-get install -y msodbcsql18 && \
    # Cleanup to keep layer size down
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Enable venv in runtime
ENV PATH="/opt/venv/bin:$PATH"

# Copy ODBC configuration
COPY odbc.ini /
RUN odbcinst -i -s -f /odbc.ini -l
RUN cat /etc/odbc.ini

# Copy application code
COPY src/ .

CMD ["python", "main.py"]
