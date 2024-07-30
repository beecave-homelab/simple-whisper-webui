FROM python:3.11-slim

# Set environment variables
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y --no-install-recommends ffmpeg \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy the application code to the container
COPY . /app

# Set the working directory
WORKDIR /app

# Create a virtual environment
RUN python -m venv $VIRTUAL_ENV

# Install the dependencies
RUN $VIRTUAL_ENV/bin/pip install --upgrade pip \
    && $VIRTUAL_ENV/bin/pip install -r requirements.txt

# Command to run the application
EXPOSE 5050
CMD ["python", "app.py"]