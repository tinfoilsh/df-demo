# Deepfake Detection Demo (Server)

## Overview
This repository contains the core deepfake detection server implementation. It provides an API for analyzing video frames to detect potential deepfakes in real-time.

## Features
- Real-time deepfake detection for video streams
- REST API for easy integration

## Prerequisites
- Python 3.8+
- Docker
- CUDA-compatible GPU (recommended for optimal performance)

## Installation

1. Build the Docker image:
   ```
   docker build -t df-demo:latest .
   ```

2. Run the container:
   ```
   docker run -p 5000:5000 df-demo:latest
   ```

## API Usage
The server exposes a REST API endpoint for deepfake detection:

```
POST /analyze
Content-Type: application/json

{
  "image": "base64_encoded_image_data"
}
```

Response:
```json
{
  "is_deepfake": true|false,
  "confidence": 0.95,
  "processing_time": "0.124s"
}
```

## Model Architecture
The deepfake detection model uses a convolutional neural network architecture optimized for identifying visual artifacts commonly present in deepfake videos. The model has been trained on a diverse dataset of real and synthetic facial videos.

## Making It Confidential
To deploy this server in a confidential computing environment, use the [confidential-df-demo](https://github.com/tinfoilsh/confidential-df-demo) repository, which wraps this implementation with Tinfoil's confidential computing platform.

## Related Repositories
- [confidential-df-demo](https://github.com/tinfoilsh/confidential-df-demo): Confidential deployment of this deepfake detection server
- [df-demo-client](https://github.com/tinfoilsh/df-demo-client): Client application for interacting with the deepfake detection service


## Contact
For more information about Tinfoil's confidential computing platform, visit [tinfoil.sh](https://tinfoil.sh)
