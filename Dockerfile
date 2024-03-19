
# Stage 1: Build and install packages
# Use a full Python image to ensure all build dependencies are available
FROM python:3.8 as builder

# Set the working directory in the builder stage
WORKDIR /build

# Copy just the requirements.txt initially to leverage Docker cache
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip wheel --no-cache-dir -w /wheels -r requirements.txt

# Stage 2: Create the runtime image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /app

# Copy the built wheels from the builder stage
COPY --from=builder /wheels /wheels

# Install the Python packages without needing to compile them
RUN pip install --no-cache /wheels/*

# Clean up the wheels
RUN rm -rf /wheels

# Copy the current directory contents into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# # Link to GitHub repository
# LABEL org.opencontainers.image.source=https://github.com/{repo_name}/book-keeping

# Run app.py when the container launches
CMD ["flask", "run"]

####################

# Multi-architecture build for the image using buildx

# # Set up a new builder instance that allows for multi-platform builds
# docker buildx create --name mymultiarchbuilder --use

# # Start up the builder instance
# docker buildx inspect --bootstrap

# Build and push the image for amd64 architecture
# docker buildx build --platform linux/amd64 \
#   -t ghcr.io/{repo_name}/book-keeping:latest \
#   --push .
