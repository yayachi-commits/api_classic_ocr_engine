# Multi-stage build for OCR API
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system dependencies for building
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libmupdf-dev \
    libpoppler-cpp-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Create wheels
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt


# Runtime stage
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /build/wheels /wheels
COPY --from=builder /build/requirements.txt .

# Install Python dependencies from wheels
RUN pip install --no-cache /wheels/*

# Copy application code
COPY app /app/app
COPY config /app/config

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:9003/health/liveness', timeout=5)"

# Run application
EXPOSE 9003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9003"]
