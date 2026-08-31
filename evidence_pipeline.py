import os
import json
import torch
import cv2
from ultralytics import YOLO
import easyocr

# ==========================================
# 1. Check GPU Availability
# ==========================================
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")
if device == 'cpu':
    print("Warning: Running on CPU only. Execution may be slow.")

# ==========================================
# 2. Initialize Models
# ==========================================
# Loads a free, pre-trained nano object detector
yolo_model = YOLO('yolov8n.pt').to(device)

# Loads EasyOCR with English language support
reader = easyocr.Reader(['en'], gpu=torch.cuda.is_available())


# ==========================================
# 3. Main Evidence Pipeline Function
# ==========================================
def process_evidence(image_path):
    """
    Runs YOLOv8 and EasyOCR on an image, combining results into 
    a structured format that NLP or Case Management modules can consume.
    """
    # --- Object Detection Step ---
    yolo_results = yolo_model(image_path, verbose=False)[0]
    
    detections = []
    for box in yolo_results.boxes:
        detections.append({
            "class_name": yolo_results.names[int(box.cls)],
            "confidence": float(box.conf),
            "bounding_box": [round(coord) for coord in box.xyxy[0].tolist()] # [xmin, ymin, xmax, ymax]
        })
        
    # --- Text Extraction Step (Patched for Python 3.14 bug) ---
    img_cv = cv2.imread(image_path)
    if img_cv is None:
        raise FileNotFoundError(f"Could not load image at path: {image_path}")
        
    # Force the image to true 2-dimensional grayscale to fix the unpack bug
    img_gray = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    ocr_results = reader.readtext(img_gray)
    
    extracted_text = []
    for (bbox, text, prob) in ocr_results:
        extracted_text.append({
            "text": text,
            "confidence": float(prob),
            "bounding_box": [[round(x), round(y)] for [x, y] in bbox]
        })
        
    # --- Return Structured Deliverable ---
    return {
        "status": "success",
        "device_used": device,
        "payload": {
            "detected_objects": detections,
            "extracted_text": extracted_text
        }
    }


# ==========================================
# 4. Execution Entry Point
# ==========================================
if __name__ == "__main__":
    # Dynamically find 'test.jpg' in the exact same folder as this script
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sample_image = os.path.join(base_dir, "test.jpg")
    
    print(f"Looking for target image at: {sample_image}")
    
    try:
        # Run pipeline
        structured_output = process_evidence(sample_image)
        
        # Print the clean structured output JSON
        print("\n--- PIPELINE OUTPUT SUCCESS ---")
        print(json.dumps(structured_output, indent=4))
        
    except Exception as e:
        print(f"\n--- PIPELINE EXECUTION ERROR ---")
        print(f"Details: {e}")
