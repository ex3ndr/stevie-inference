# Use the official CUDA base image
FROM nvidia/cuda:12.3.2-runtime-ubuntu22.04

# Set the working directory
WORKDIR /app

# Install git-lfs repository
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash

# Install any necessary dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git-core \
    git-lfs \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Add the requirements file to the container
COPY requirements.txt /app

# Install the required Python packages
RUN pip3 install -r requirements.txt && pip3 install git+https://github.com/m-bain/whisperx.git
RUN pip3 install ctranslate2==4.5.0

# Set the environment variable for production
ENV PRODUCTION=1

# Add the rest of your code to the container
COPY . /app

ENV LD_LIBRARY_PATH=/usr/local/lib/python3.10/dist-packages/nvidia/cublas/lib:/usr/local/lib/python3.10/dist-packages/nvidia/cudnn/lib
RUN find ~/ -name libcudnn_ops_infer.so.8
# RUN python3 -c 'import os; import nvidia.cublas.lib;import nvidia.cudnn.lib; print(os.path.dirname(nvidia.cublas.lib.__file__) + ":" + os.path.dirname(nvidia.cudnn.lib.__file__))'

# Set the entry point for running your inference code
CMD ["python3", "-u", "app.py"]