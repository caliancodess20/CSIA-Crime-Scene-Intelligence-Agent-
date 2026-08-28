import os
import json
import torch
import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from ultralytics import YOLO
import easyocr

# Initialize FastAPI application
app = FastAPI(title="Crime Scene Intelligence Detector API")

# Initialize models globally
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Service running on: {device}")

yolo_model = YOLO('yolov8n.pt').to(device)
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())

@app.post("/analyze-evidence/")
async def analyze_evidence(file: UploadFile = File(...)):
    try:
        # Read the uploaded file bytes directly into memory
        file_bytes = await file.read()
        nparr = np.frombuffer(file_bytes, np.uint8)
        img_cv = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img_cv is None:
            return JSONResponse(status_code=400, content={"error": "Invalid image file uploaded."})

        # --- 1. YOLOv8 Object Detection ---
        yolo_results = yolo_model(img_cv, verbose=False)
        detections = []
        for box in yolo_results[0].boxes:
            detections.append({
                "class_name": yolo_results[0].names[int(box.cls)],
                "confidence": float(box.conf[0]),
                "bounding_box": [round(coord) for coord in box.xyxy[0].tolist()]
            })
            
        # --- 2. EasyOCR Text Extraction (Patched for 3.14 Unpack Bug) ---
        img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
        ocr_results = reader.readtext(img_gray)
        
        extracted_text = []
        for (bbox, text, prob) in ocr_results:
            extracted_text.append({
                "text": text,
                "confidence": float(prob),
                "bounding_box": [[round(x), round(y)] for [x, y] in bbox]
            })
            
        # --- 3. Return Structured Response ---
        return {
            "status": "success",
            "device_used": device,
            "filename": file.filename,
            "payload": {
                "detected_objects": detections,
                "extracted_text": extracted_text
            }
        }
        
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "error", "message": str(e)})

if __name__ == "__main__":
    import uvicorn
    # Starts the local server
    uvicorn.run(app, host="127.0.0.1", port=8000)
