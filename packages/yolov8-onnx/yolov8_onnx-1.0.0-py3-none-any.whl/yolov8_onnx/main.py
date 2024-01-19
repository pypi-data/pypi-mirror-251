# RE-WRITER/WRITER: LauNT # EMAIL: ttruongllau@gmail.com 

from yolov8_onnx.centers import Detector
import traceback


class DetectEngine():
    def __init__(self, model_path = None,
                 image_size = 640,
                 conf_thres = 0.5, 
                 iou_thres  = 0.1) -> None:
        self.detector = Detector(model_path, image_size, conf_thres, iou_thres)


    def __call__(self, image) -> tuple:
        det_res = None
        try:
            det_res = self.detector(image)
        except Exception:
            print(traceback.format_exc())
        return det_res