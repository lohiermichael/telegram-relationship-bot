# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

# Copy the requirements file into the container
COPY docker/prod/requirements.txt /app/

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code
COPY ../../src ./src

# Expose a port for your app (if needed)
EXPOSE 8000

# Command to run the production app
CMD ["python", "src/main.py"]
