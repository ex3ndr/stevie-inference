# Use the official CUDA base image
FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install gitlfs dependency repo
RUN curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git-core \
    git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Add the requirements file to the container
COPY requirements.txt /app

# Install the required Python packages
RUN pip3 install -r requirements.txt

# Set the environment variable for production
ENV PRODUCTION=1

# Add the rest of your code to the container
COPY . /app

# Set the entry point for running your inference code
CMD ["python3", "-u", "app.py"]