# Use official slim Python 3.12 image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies required for mysqlclient, Pillow, and netcat
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    libjpeg-dev \
    zlib1g-dev \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project source code
COPY . /app/

# Ensure entrypoint script is executable and uses Unix LF line endings
RUN dos2unix /app/entrypoint.sh && chmod +x /app/entrypoint.sh

# Expose Django port
EXPOSE 8000

# Set entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Default command
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
