# Classic OCR Engine - FastAPI Microservice

A FastAPI-based microservice for document OCR and text extraction. Supports PDF, DOCX, HTML, and TXT formats with optional OCR capabilities for image-based PDFs.

## Features

- 📄 **Multi-Format Support**: PDF, DOCX, HTML, TXT
- 🔍 **OCR Capabilities**: Optional Tesseract OCR for image-based PDFs
- 📦 **Clean API**: RESTful endpoints with structured responses
- 🔐 **Security**: Request validation, CORS support, rate limiting ready
- 📊 **Observability**: Request tracking, health checks, structured logging
- 🚀 **Production Ready**: Docker support, configuration management, error handling

## Quick Start

### Prerequisites

- Python 3.11+
- Tesseract OCR (for OCR features)
- libmupdf (for PDF processing)

### Installation

1. Clone the repository:
```bash
cd ~/api_classic_ocr_engine
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create `.env` from `.env.example`:
```bash
cp .env.example .env
```

5. Run the application:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 9003
```

The API will be available at `http://localhost:9003`

## API Endpoints

### Health Checks

- `GET /health/liveness` - Liveness probe
- `GET /health/readiness` - Readiness probe

### Conversion

- `GET /api/v1/convert/formats` - List supported formats
- `POST /api/v1/convert` - Convert document to text

### Example Usage

```bash
# List supported formats
curl http://localhost:9003/api/v1/convert/formats

# Convert a PDF
curl -X POST http://localhost:9003/api/v1/convert \
  -F "file=@document.pdf" \
  -F "use_ocr=true"

# Convert a DOCX with specific format
curl -X POST http://localhost:9003/api/v1/convert \
  -F "file=@document.docx" \
  -F "format=docx"
```

## Configuration

Configuration is managed via environment variables. See `.env.example` for all available options:

### Core Settings
- `APP_NAME` - Service name (default: "Classic OCR Engine")
- `APP_ENV` - Environment (dev/prod)
- `DEBUG` - Debug mode (default: false)
- `LOG_LEVEL` - Logging level (DEBUG/INFO/WARNING/ERROR/CRITICAL)

### Server Settings
- `HOST` - Server host (default: 0.0.0.0)
- `PORT` - Server port (default: 9003)
- `API_PREFIX` - API route prefix (default: /api/v1)
- `REQUEST_TIMEOUT_SECONDS` - Request timeout (default: 300)

### OCR Settings
- `MAX_FILE_SIZE_MB` - Maximum file size (default: 100)
- `SUPPORTED_FORMATS` - Comma-separated list of supported formats
- `ENABLE_OCR` - Enable OCR by default (default: true)

## Docker

### Build Image

```bash
docker build -t api-classic-ocr-engine:latest .
```

### Run Container

```bash
docker run -p 9003:9003 \
  -e APP_ENV=prod \
  -e LOG_LEVEL=INFO \
  api-classic-ocr-engine:latest
```

## Project Structure

```
api_classic_ocr_engine/
├── app/
│   ├── __init__.py
│   ├── main.py              # ASGI entrypoint
│   ├── app.py               # FastAPI app configuration
│   ├── clients/             # External service clients
│   ├── internal/
│   │   ├── config.py        # Settings management
│   │   ├── logs.py          # Logging setup
│   │   └── models.py        # Pydantic models
│   ├── orchestrator/
│   │   ├── converter.py     # Document conversion logic
│   │   └── manager.py       # Conversion manager
│   └── routers/
│       └── convert.py       # API endpoints
├── config/                  # Configuration files
├── test/                    # Test files
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

## Response Format

All responses follow a consistent JSON format:

### Success Response
```json
{
  "success": true,
  "input_file": "document.pdf",
  "file_format": "pdf",
  "lines_extracted": 42,
  "text_content": "...",
  "request_id": "uuid-here"
}
```

### Error Response
```json
{
  "success": false,
  "error_code": "UNSUPPORTED_FORMAT",
  "message": "File format 'xyz' not supported",
  "request_id": "uuid-here"
}
```

## Development

### Running Tests

```bash
pytest test/
```

### Code Quality

```bash
# Format code
black app/

# Lint code
pylint app/

# Type checking
mypy app/
```

## System Requirements

### Required
- Python 3.11+
- libmupdf (for PDF support)

### Optional
- tesseract-ocr (for OCR features)
- Additional fonts for better OCR accuracy

### Linux Installation

```bash
# Ubuntu/Debian
sudo apt-get install libmupdf-dev tesseract-ocr

# Fedora
sudo dnf install mupdf-devel tesseract

# macOS
brew install mupdf-tools tesseract
```

## Performance Considerations

- **File Size**: Default max is 100 MB (configurable)
- **Timeout**: Default 300 seconds per request (configurable)
- **Concurrency**: Scales with uvicorn workers
- **OCR**: Can be slow for large PDFs; disable if not needed

## Troubleshooting

### Tesseract Not Found
```bash
# Linux
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract

# Set PYTESSERACT_PATH environment variable if needed
export PYTESSERACT_PATH=/usr/bin/tesseract
```

### Out of Memory on Large PDFs
- Reduce `MAX_FILE_SIZE_MB`
- Disable OCR (`ENABLE_OCR=false`)
- Process files in batches

### LibMuPDF Build Issues
```bash
pip install --upgrade pymupdf
```

## License

Proprietary - Internal Use Only

## Contributing

See CLAUDE.md for development guidelines.
