# Use Python base image
FROM --platform=linux/amd64 python:3.9-slim

# Set working directory
WORKDIR /app

# Copy code and requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Expose Flask's port
ENV PORT=8080
EXPOSE 8080

# Allow running any Python service file via environment variable
CMD ["sh", "-c", "python ${SERVICE_FILE}"]