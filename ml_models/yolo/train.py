from ultralytics import YOLO
model = YOLO('yolov8n.pt')
if __name__ == '__main__':
    model.train(data='ml_models/yolo/dataset.yaml', epochs=10, imgsz=640)
