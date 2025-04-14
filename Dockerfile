FROM python:3.10

WORKDIR /app

# Install system dependencies for OpenCV
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy server code
COPY server.py .

# Create temp directory for uploads
RUN mkdir -p temp_uploads

# Expose the port the app runs on
EXPOSE 8080

# Command to run the application
CMD ["python", "server.py"]