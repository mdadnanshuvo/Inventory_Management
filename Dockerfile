# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for PostGIS, GDAL, and PostgreSQL
# Install system dependencies for PostGIS, GDAL, and PostgreSQL
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    gdal-bin \
    libgdal-dev \
    postgis \
    postgresql-client \
    python3-dev \
    libproj-dev \
    libgeos-dev \
    gettext \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*


# Set GDAL version as an environment variable to avoid issues with Django/GDAL binding
ENV GDAL_VERSION=3.4.1  
ENV GDAL_LIBRARY_PATH=/usr/lib/x86_64-linux-gnu/libgdal.so

# Install Python dependencies from requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the project files into the container
COPY . /app/

# Copy the entrypoint script into the container
COPY entrypoint.sh /app/entrypoint.sh

# Set execute permissions for the entrypoint script
RUN chmod +x /app/entrypoint.sh

# Expose port 8000 (or whichever port you need for Django)
EXPOSE 8000

# Set the entrypoint for the container
ENTRYPOINT ["/app/entrypoint.sh"]

# Set the command to run the Django app
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
