# Specify base ikmage for docker container
# Use FROM python to create a new image from scratch
FROM python:3.14-rc-bookworm

# Use FROM existing_image_name to take reference of any existing image and build new image based on existing image
#FROM forecast

# Install required system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    cmake \
    gcc \
    g++ \
    libopenblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Sets working directory inside docker container
WORKDIR /forecasting_dir

# Below lines ensures that pip is upgraded to latest version
RUN python -m pip install --upgrade pip
RUN pip install --upgrade pip setuptools setuptools_scm wheel

# Run requirements.txt recursively to install all required libraries
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --prefer-binary -r requirements.txt

# Copy entire project folder from local machine to container
COPY . .

# Define entry point for Flask application
ENV FLASK_APP=app.py

# Specify default command to run when container starts
CMD ["python","-m","flask","run","--host=0.0.0.0"]

# To build docker container run in terminal --> docker build -t <tag_name>
# To start docker container run in terminal --> docker run -p <docker_port>:<local_machine_port(5000 for flask)> -d <tag_name>
