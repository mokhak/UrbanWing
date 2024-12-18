# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5004

ENV PORT=5004

# Allow running any Python service file via environment variable
CMD ["python", "camera.py"]