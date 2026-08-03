# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Upgrade pip (the script only uses the Python standard library, so there are no
# third-party packages to install)
RUN pip install --no-cache-dir --upgrade pip

# Command to run the script
CMD ["python", "analyze_data.py"]
