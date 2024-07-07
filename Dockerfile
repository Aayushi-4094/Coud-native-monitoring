# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirement.txt .

# Install the dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirement.txt

# Copy the rest of the application code into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_RUN_HOST=0.0.0.0

# Expose port 5000 to the host
EXPOSE 5000

# Define the command to run the application
CMD ["flask", "run"]
