from fastapi import FastAPI, File, UploadFile
import cv2
from fastapi.staticfiles import StaticFiles
import numpy as np
from io import BytesIO
from starlette.responses import JSONResponse, FileResponse
import base64

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

def remove_background(image_bytes):
    image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), cv2.IMREAD_UNCHANGED)

    # Background removal logic...
    lower = np.array([200, 200, 200])
    upper = np.array([255, 255, 255])
    thresh = cv2.inRange(image, lower, upper)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (20, 20))
    morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    mask = 255 - morph

    if image.shape[2] < 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
    
    image[:, :, 3] = cv2.bitwise_and(image[:, :, 3], mask)
    
    # Convert the images to base64
    _, image_encoded = cv2.imencode('.png', image)
    _, mask_encoded = cv2.imencode('.png', mask)

    image_base64 = base64.b64encode(image_encoded).decode('utf-8')
    mask_base64 = base64.b64encode(mask_encoded).decode('utf-8')

    return {'image': image_base64, 'mask': mask_base64}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    result = remove_background(file_bytes)
    return JSONResponse(content=result)

@app.get("/")
def read_root():
    return FileResponse('templates/index.html')

