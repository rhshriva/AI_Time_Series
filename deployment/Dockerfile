# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set environment variables (if needed)
# ENV SOME_ENV_VAR=some_value

# Default command to run the metrics collector
CMD ["python", "gpu_metrics_collector.py"]
