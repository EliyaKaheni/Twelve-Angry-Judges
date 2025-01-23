# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Install MySQL client (required for mysql-connector-python)
RUN apt-get update && apt-get install -y default-libmysqlclient-dev && rm -rf /var/lib/apt/lists/*

# Expose the port your application will run on
EXPOSE 8000

# Set the command to run your application
CMD ["uvicorn", "Back:app", "--host", "0.0.0.0", "--port", "8000"]