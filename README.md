# MarkItDown API

MarkItDown API is a lightweight service built with FastAPI for converting files or URLs into Markdown using Microsoft's MarkItDown library. The API supports multiple file formats, such as PDF, DOCX, XLSX, and more.

---

## Features

- **File Conversion**: Upload a file and convert it to Markdown format.
- **URL Conversion**: Provide a URL to download and convert a file to Markdown.

## Requirements

- Python 3.10
- Docker (for containerized deployment)



### Local Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/jabahm/markitdown-api.git
   cd markitdown-api
   ```
2. Create a virtual environment and activate it:
   ```bash
    python3 -m venv venv
    source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
    pip install -r requirements.txt
   ```
4. Run the FastAPI server:
   ```bash
    uvicorn main:app --reload
   ```
The API will be available at http://127.0.0.1:8000.

### Docker Installation

4. Build the Docker image:
```bash
docker build -t markitdown-api .
```
4. Run the Docker container:
```bash
docker run -p 8000:8000 markitdown-api
```
Access the API at http://127.0.0.1:8000.

