# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Copy the application code into the container
COPY . .


# Install the application dependencies
RUN apt-get update && apt-get install -y dos2unix
RUN pip install --no-cache-dir -r requirements.txt
RUN dos2unix server_run.bash


# Run the application
CMD ["bash", "server_run.bash", "deploy"]