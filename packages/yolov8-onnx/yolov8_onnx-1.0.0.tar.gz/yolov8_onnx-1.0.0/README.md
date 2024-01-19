# YOLOV8 ONNX

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python 3.7](https://img.shields.io/badge/Python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/)
[![ONNX Compatible](https://img.shields.io/badge/ONNX-Compatible-brightgreen)](https://onnx.ai/)

## Description

This package is compatible with [YoloV8](https://github.com/ultralytics/ultralytics) for object detection program, using [ONNX](https://onnx.ai/) format model (CPU speed can be x2 times faster). This code is referenced from [this awesome repo](https://github.com/ibaiGorordo/ONNX-YOLOv8-Object-Detection).

## Installation

You can install the package using pip:

```bash
pip install yolov8_onnx
```

## Usage

Step 1: Convert your pre-trained model to ONNX format.

```python
from ultralytics import YOLO

# Load your pre-trained model
model = YOLO('your-trained-model.pt')

# Export the model
model.export(format='onnx', imgsz=640, dynamic=True)
```

Step 2: Use in your code.

```python
from yolov8_onnx import DetectEngine

engine = DetectEngine(model_path='your-model.onnx', conf_thres=0.5, iou_thres=0.1)

output = engine(image) # cv2 image
```

## License

This project is licensed under the Apache License 2.0 - see the LICENSE file for details.

" I hope this package will be useful for your projects" Nguyễn Trường Lâu (from [akaOCR](https://app.akaocr.io/)).