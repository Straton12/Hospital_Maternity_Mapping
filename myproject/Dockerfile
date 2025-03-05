# Use Python 3.11 on Alpine Linux as the base image
FROM python:3.11-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache \
    gcc \
    musl-dev \
    libffi-dev \
    postgresql-dev \
    gdal \
    gdal-dev \
    geos \
    geos-dev \
    proj \
    proj-dev \
    python3-dev \
    py3-pip \
    py3-setuptools \
    py3-wheel

# Ensure GDAL is linked properly
RUN ln -s /usr/lib/libgdal.so /usr/lib/libgdal.so.30 || true


RUN apk add --no-cache postgresql postgresql-contrib postgis postgresql-client


# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /myproject/

# Set up static/media directories and user permissions
RUN mkdir -p /vol/web/media /vol/web/static && \
    adduser -D user && \
    chown -R user:user /vol && \
    chmod -R 755 /vol

# Copy and set up the entrypoint script
COPY myproject/scripts /scripts
RUN chmod +x /scripts/*

USER user

# Expose the port Django runs on
EXPOSE 8000

# Run the entrypoint script
ENTRYPOINT ["/scripts/entrypoint.sh"]
