# Use the official CUDA base image
FROM nvidia/cuda:11.4.0-base

# Set the working directory
WORKDIR /app

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Copy your AI inference code to the container
COPY . /app

# Install the required Python packages
RUN pip3 install -r requirements.txt

# Set the entry point for running your inference code
CMD ["python3", "server.py"]