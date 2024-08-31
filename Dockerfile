# Use the official Python image from the Docker Hub
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary packages
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir jsonlines

# Command to run the script
CMD ["python", "analyze_data.py"]
