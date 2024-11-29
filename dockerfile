# Use a Python base image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        gcc \
        libffi-dev \
        libssl-dev \
        python3-dev \
        default-libmysqlclient-dev \
        pkg-config \
    && python -m pip install --upgrade pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# Copy and install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose port (adjust as necessary)
EXPOSE 8000

# Run migrations and collect static files (adjust as necessary)
RUN python manage.py migrate
RUN python manage.py collectstatic --no-input

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
