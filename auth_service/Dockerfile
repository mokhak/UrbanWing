# Use Python base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV PORT=8080

# Allow running any Python service file via environment variable
CMD ["python", "auth.py"]