# RE-WRITER/WRITER: LauNT # EMAIL: ttruongllau@gmail.com 

import numpy as np
import onnxruntime
import cv2
import math

from .utility import post_processing_output


class Detector(object):

    def __init__(self, model_path=None, img_size=640, 
                 conf_thres=0.5, iou_thres=0.1):
         # Initialize model

        self.conf_threshold = conf_thres
        self.iou_threshold = iou_thres
        self.img_size = img_size
        self.initialize_model(model_path)

    
    def __call__(self, image):
        # Object detection

        input_tensor, img_shape, model_shape  = self.prepare_input(image)
        (img_w, img_h), (model_w, model_h) = img_shape, model_shape

        # model inference
        outputs = self.session.run(
            self.output_names, 
            {self.input_names[0]: input_tensor}
        )

        self.boxes, self.scores, self.class_ids = post_processing_output(
            outputs,
            (img_w, img_h), 
            (model_w, model_h),
            self.conf_threshold,
            self.iou_threshold
        )

        return self.boxes, self.scores, self.class_ids


    def initialize_model(self, model_path):
        # Get model informations

        assert model_path != None, "Error: model not found!"

        self.session = onnxruntime.InferenceSession(
            model_path, providers=['CPUExecutionProvider'])
        
        self.get_input_infors()
        self.get_output_infors()

    
    def get_input_infors(self):
        # Get input infors of model

        model_inputs = self.session.get_inputs()
        self.input_names = [
            model_inputs[i].name 
            for i in range(len(model_inputs))
        ]


    def get_output_infors(self):
        # Get output infors of model

        model_outputs = self.session.get_outputs()
        self.output_names = [
            model_outputs[i].name 
            for i in range(len(model_outputs))
        ]

    def prepare_input(self, image):
        # Prepare input tensor

        img_height, img_width = image.shape[:2]
        ratio = self.img_size / max(img_height, img_width)

        # get input_w & input_h for model
        w = min(math.ceil(img_width * ratio), self.img_size)
        h = min(math.ceil(img_height * ratio), self.img_size)

        if w < h: w = math.ceil(w / 32) * 32
        if w > h: h = math.ceil(h / 32) * 32

        # resize input image
        input_img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_img = cv2.resize(input_img, (w, h))

        # scale input pixel values to 0 to 1
        input_img = input_img / 255.0
        input_img = input_img.transpose(2, 0, 1)
        input_tensor = input_img[np.newaxis, :, :, :].astype(np.float32)

        return input_tensor, (img_width, img_height), (w, h)
