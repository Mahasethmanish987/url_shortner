# Use official lightweight Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential && \
    rm -rf /var/lib/apt/lists/*

# Copy dependency file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the Django project
COPY . /app/

# Expose port (Render maps automatically)
EXPOSE 8000

# Collect static files
RUN python manage.py collectstatic --noinput

# Run the Django app with Gunicorn
CMD ["gunicorn", "urlshortner.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1"]

