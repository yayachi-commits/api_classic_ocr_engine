#!/bin/bash
# Local Docker build and run script for Classic OCR Engine

set -e

IMAGE_NAME="api-classic-ocr-engine"
IMAGE_TAG="latest"
CONTAINER_NAME="classic-ocr-engine"
PORT=9003

echo "=========================================="
echo "Classic OCR Engine - Docker Build & Run"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}Error: Docker is not running${NC}"
    exit 1
fi

# Build the image
echo -e "${YELLOW}Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}${NC}"
docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .

if [ $? -ne 0 ]; then
    echo -e "${RED}Build failed${NC}"
    exit 1
fi

echo -e "${GREEN}Build successful${NC}"

# Stop existing container if running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo -e "${YELLOW}Stopping existing container: ${CONTAINER_NAME}${NC}"
    docker stop ${CONTAINER_NAME} 2>/dev/null || true
    docker rm ${CONTAINER_NAME} 2>/dev/null || true
fi

# Run the container
echo -e "${YELLOW}Starting container: ${CONTAINER_NAME}${NC}"
docker run -d \
    --name ${CONTAINER_NAME} \
    -p ${PORT}:9003 \
    -e APP_ENV=dev \
    -e LOG_LEVEL=INFO \
    -e DEBUG=true \
    -e DOCS_ENABLED=true \
    ${IMAGE_NAME}:${IMAGE_TAG}

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to start container${NC}"
    exit 1
fi

echo -e "${GREEN}Container started successfully${NC}"

# Wait for container to be ready
echo -e "${YELLOW}Waiting for service to be ready...${NC}"
sleep 3

# Check health
if curl -s http://localhost:${PORT}/health/liveness > /dev/null; then
    echo -e "${GREEN}Service is healthy and ready${NC}"
    echo -e "${GREEN}=========================================="
    echo -e "Classic OCR Engine is running!"
    echo -e "API URL: http://localhost:${PORT}"
    echo -e "API Docs: http://localhost:${PORT}/docs"
    echo -e "Redoc: http://localhost:${PORT}/redoc"
    echo -e "==========================================${NC}"
else
    echo -e "${YELLOW}Service is starting, please wait...${NC}"
fi

# Show logs
echo -e "${YELLOW}Container logs:${NC}"
docker logs -f ${CONTAINER_NAME}
