FROM debian:latest

# Update the package list and install basic utilities
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Install Twitter Crawler 
RUN curl -sL https://deb.nodesource.com/setup_18.x | bash -
RUN apt-get install nodejs -y
RUN npx playwright install-deps

CMD ["bash"]
