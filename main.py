from fastapi import FastAPI, UploadFile, File, HTTPException
from markitdown import MarkItDown
import shutil
import os
import requests

app = FastAPI(title="MarkItDown API", description="Convert files or URLs to Markdown using Microsoft's MarkItDown.")


@app.post("/convert/file/")
async def convert_file_to_markdown(file: UploadFile = File(...)):
    """
    Upload a file to convert it into Markdown using MarkItDown.
    Supported formats: PDF, DOCX, XLSX, Images, etc.
    """
    temp_file = None
    try:
        temp_file = f"temp_{file.filename}"
        with open(temp_file, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        md = MarkItDown()
        result = md.convert(temp_file)

        return {"filename": file.filename, "markdown": result.text_content}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)

@app.post("/convert/url/")
async def convert_url_to_markdown(url: str):
    """
    Provide a URL to download a file and convert it into Markdown using MarkItDown.
    Supported formats: PDF, DOCX, XLSX, Images, etc.
    """
    temp_file = None
    try:
        if not url.startswith(("http://", "https://")):
            raise HTTPException(status_code=400, detail="Invalid URL. Must start with http:// or https://")

        response = requests.get(url, stream=True, allow_redirects=True)
        if response.status_code != 200:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to download file from URL. Status code: {response.status_code}"
            )

        filename = "downloaded_file"
        if "Content-Disposition" in response.headers:
            content_disposition = response.headers["Content-Disposition"]
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[-1].strip().strip('"')
        else:
            filename = url.split("/")[-1] or "downloaded_file"

        temp_file = f"temp_{filename}"
        with open(temp_file, "wb") as buffer:
            for chunk in response.iter_content(chunk_size=1024 * 8):
                buffer.write(chunk)

        md = MarkItDown()
        result = md.convert(temp_file)

        return {"filename": filename, "markdown": result.text_content}

    except requests.RequestException as req_err:
        raise HTTPException(status_code=400, detail=f"Request error: {str(req_err)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)



