import io
import os
import cv2
import numpy as np

import uvicorn
import nest_asyncio
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse, Response

from handlers import watermark


app = FastAPI(title="Image Watermarking")


@app.get("/")
def home():
    return "FastAPI working. Head to https://localhost:8000/docs"


@app.post("/watermark")
def apply_watermark(text: str = 'Watermarked',
                    font_size: int = 1,
                    color: str = '255, 255, 255',
                    thickness: int = 1,
                    file: UploadFile = File(...)):
    # 1. Validate input file
    filename = file.filename
    fileExtension = filename.split(".")[-1] in ("jpg", "jpeg", "png", "tif")
    if not fileExtension:
        raise HTTPException(
            status_code=415, detail="Unsupported file provided.")

    if not font_size or not color or not thickness:
        raise HTTPException(
            status_code=415, detail="Please input enough information")
    if color:
        color = tuple(int(c) for c in color.strip().split(','))

    # 2. Transform raw image into cv2 image
    image_stream = io.BytesIO(file.file.read())
    image_stream.seek(0)

    file_bytes = np.asarray(bytearray(image_stream.read()), dtype=np.uint8)

    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

    # 3. Water mark image
    watermark_image = watermark(image, text, font_size, color, thickness)
    cv2.imwrite(f'watermark_images/{filename}', watermark_image)

    # 4. Stream the response back to the client
    file_image = open(f'watermark_images/{filename}', mode="rb")

    return StreamingResponse(file_image, media_type="image/jpeg")


if __name__ == "__main__":
    nest_asyncio.apply()
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"
    uvicorn.run(app, host=host, port=8000)
