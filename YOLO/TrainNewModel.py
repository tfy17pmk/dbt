from ultralytics import YOLO

# Load a model
model = YOLO("best-2.pt")  # load a pretrained model (recommended for training)

# Train the model
results = model.predict(source=0, stream=False, device="mps", imgsz=640, )

'''for result in model.predict(source=0, stream=False, device="mps"):
    print(result.speed)'''