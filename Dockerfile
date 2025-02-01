# Specify base ikmage for docker container
FROM python:3.14-rc-bookworm

# Sets working directory inside docker container
WORKDIR /forecasting_dir

# Copy entire project folder from local machine to container
COPY . .
# Below lines ensures that pip is upgraded to latest version
RUN python -m pip install --upgrade pip
# Run requirements.txt recursively to install all required libraries
RUN pip install -r requirements.txt

# Define entry point for Flask application
ENV FLASK_APP=app.py

# Specify default command to run when container starts
CMD ["python","-m","flask","run","--host=0.0.0.0"]

# To build docker container run in terminal --> docker build -t <tag_name>
# To start docker container run in terminal --> docker run -p <docker_port>:<local_machine_port(5000 for flask)> -d <tag_name>
