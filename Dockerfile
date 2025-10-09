# Use a small Python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy and install dependencies first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY calculator.py .

# Default command runs the CLI app
ENTRYPOINT ["python", "calculator.py"]

