# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set environment variables to prevent interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o /tmp/install.sh && \
    sh /tmp/install.sh -y -q && \
    rm /tmp/install.sh && \
    ~/.cargo/bin/rustup default stable

# Create a non-root user
RUN useradd -m 1filellm

# Switch to the non-root user
USER 1filellm


# Set the working directory
WORKDIR /home/1filellm

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY onefilellm.py .

# Set the default command to run the application
CMD ["python", "onefilellm.py"]

