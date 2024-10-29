# Use a specific Python version tag for consistency
FROM python:3.12-slim

# Set environment variables for non-interactive installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies and Rust
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        curl \
        ca-certificates \
        libssl-dev \
        && curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs -o /tmp/install.sh && \
    sh /tmp/install.sh -y && \
    rm -rf /var/lib/apt/lists/* /tmp/install.sh

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -U -r /tmp/requirements.txt && \
    rm /tmp/requirements.txt

# Create a non-root user for running the application
RUN useradd -m 1filellm

# Set the working directory
WORKDIR /1filellm

# Copy the application code
COPY onefilellm.py .

# Change ownership of the working directory to the non-root user
RUN chown -R 1filellm:1filellm /1filellm

# Switch to the non-root user
USER 1filellm

# Set the command to run the application
CMD ["python", "onefilellm.py"]

