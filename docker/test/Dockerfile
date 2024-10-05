# Use an official Python runtime as a base image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Set environment variables for Python
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=.

# Copy the requirements file into the container
COPY docker/test/requirements.txt /app/

# Install the dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire source code
COPY ../../src ./src
COPY ../../tests ./tests

# Expose a port for your app (if necessary)
EXPOSE 8000

# Default command to run tests with pytest and auto-reload on file changes
CMD ["watchmedo", "auto-restart", \
     "--patterns=*.py", \
     "--recursive", \
     "--debounce-interval=2", \
     "--no-restart-on-command-exit", \
     "--", "pytest", "tests/"]
