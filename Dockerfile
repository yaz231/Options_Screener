# Use the official Python base image
FROM python:3.9-slim

# Install required system dependencies
RUN apt-get update \
    && apt-get install -y libxml2-dev libxslt-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /code

# Copy the requirements.txt file into the container
COPY requirements.txt /code/requirements.txt

# Install project dependencies
RUN pip install -r /code/requirements.txt

# Copy the entire project directory into the container
COPY ./app /code/app

# Copy the templates directory into the container
COPY ./templates /code/templates

# Expose the port your application runs on (replace 8000 with your application's port)
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]