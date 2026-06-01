FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=run.py

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy project files
COPY . /app/

# Expose port
EXPOSE 5000

# Run migrations and start server
CMD ["sh", "-c", "mkdir -p instance && flask db upgrade && gunicorn -b 0.0.0.0:5000 run:app"]
