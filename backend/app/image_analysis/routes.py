import os
import shutil
from fastapi import APIRouter, UploadFile, File
from backend.app.image_analysis.yolo_detector import detect_objects
from backend.app.image_analysis.ocr_reader import extract_text
router = APIRouter(prefix="/image-analysis", tags=["Image Analysis"])
@router.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    temp_path = f"temp_{file.filename}"
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    try:
        detections = detect_objects(temp_path)
        ocr_results = extract_text(temp_path)
        return {
            "status": "success",
            "detections": detections,
            "ocr": ocr_results
        }
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
