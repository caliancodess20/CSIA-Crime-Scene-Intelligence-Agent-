import cv2
from ultralytics import YOLO
model = YOLO('yolov8n.pt')
def detect_objects(image_path: str):
    results = model(image_path)
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": model.names[int(box.cls[0])],
                "confidence": round(float(box.conf[0]), 2),
                "bbox": [round(x, 2) for x in box.xyxy[0].tolist()]
            })
    return detections
