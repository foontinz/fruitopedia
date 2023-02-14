# Use an official Python runtime as the base image
FROM python:3.11

# Set the working directory in the container
WORKDIR /

# Copy the application code into the container
COPY . .

# Install the application dependencies
RUN pip install --no-cache-dir -r requirements.txt



# Run the application
CMD ["bash", "server_run.sh"]