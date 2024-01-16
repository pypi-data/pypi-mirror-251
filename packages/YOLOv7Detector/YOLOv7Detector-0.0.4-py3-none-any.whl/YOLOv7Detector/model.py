# Now try importing
import random  # Random colours
import cv2  # showing result detections
import numpy as np
from PIL import Image
import torch
import sys
import os
import warnings
import traceback

warnings.filterwarnings('ignore', category=UserWarning)

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'yolov7')))

from YOLOv7Detector.yolov7.models.experimental import attempt_load
from YOLOv7Detector.yolov7.utils.general import non_max_suppression, scale_coords
from YOLOv7Detector.yolov7.utils.plots import plot_one_box
from YOLOv7Detector.yolov7.utils.torch_utils import TracedModel
from YOLOv7Detector.yolov7.utils.datasets import letterbox

from YOLOv7Detector.image_funcs import resize_image, recolor_image


class Detector():
    """
    This class is a wrapper for the YOLOv7 model.

    """

    def __init__(self, weights_path='yolov7.pt', conf_thres=0.7, iou_thres=0.45, img_size=640):

        # Args
        self.img_size = img_size
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.weights_path = weights_path

        # KEEP ON CPU - NOT TESTED ON GPU
        self.device = 'cpu'

        self.stride = 0
        self.detector_model = None
        self.names = None

        self.build_detector()

        self.colors = [[random.randint(0, 255) for _ in range(3)] for _ in self.names]

    def build_detector(self):

        # check if the weights file exists
        if not os.path.isfile(self.weights_path):
            raise FileNotFoundError("Weights file not found at {}".format(self.weights_path))

        model = attempt_load(self.weights_path, map_location=self.device)  # load FP32 model

        try:
            self.stride = int(model.stride.max())  # model stride
        except Exception as e:
            warnings.warn("Could not get stride from model, defaulting to 32")

        try:
            self.detector_model = TracedModel(model, self.device, self.img_size)
        except Exception as e:
            raise Exception(f"Could not trace model, {traceback.format_exc()}")

        self.names = self.detector_model.module.names if hasattr(self.detector_model,
                                                                 'module') else self.detector_model.names

        if self.names is None:
            raise Exception("Names not found in model")

    def preprocess_image(self, image):

        # Padded resize
        im0 = np.array(image.convert('RGB'))  # not actually rgb, its bgr
        img = letterbox(im0, self.img_size, stride=self.stride)[0]

        # Convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(self.device)
        img = img.float()
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        return img, im0

    def calculateDetections(self, image, view_img=False, download_path=None):
        """
        This function takes an image and returns a list of detections. Each detection is a dictionary with the following keys:
        - class: The class of the detection
        - confidence: The confidence of the detection
        - bbox: The bounding box of the detection in the format [x1, y1, x2, y2]

        :param image: PIL image
        :param view_img: bool, whether to show the image with the detections
        :param download_path: string pointing to download path. Leave as None if not needed (make sure to add extension, eg .jpg)
        :return: list of dicts of the results.
        """

        # convert to numpy
        img, im0 = self.preprocess_image(image)  # im0 is the original image converted to numpy

        with torch.no_grad():
            pred = self.detector_model(img)[0]

        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=0, agnostic=False)

        dets = self.process_detections(pred, im0, img, view_img=view_img, download_path=download_path)

        return dets

    def process_detections(self, pred, im0s, img, view_img, download_path=None):
        s = ''
        dets = []
        # Process detections
        for i, det in enumerate(pred):  # detections per image
            im0 = im0s

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {self.names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):

                    dets.append({
                        "class": self.names[int(cls)],
                        "confidence": conf.item(),  # Convert from tensor to float
                        "bbox": [val.item() for val in xyxy]  # Convert bounding box tensor to list
                    })

                    if view_img:  # Add bbox to image
                        label = f'{self.names[int(cls)]} {conf:.2f}'
                        plot_one_box(xyxy, im0, label=label, color=self.colors[int(cls)], line_thickness=1)

            # Stream results
            if download_path or view_img:
                det_img = recolor_image(resize_image(im0))

            if view_img:
                cv2.imshow('image', det_img)
                cv2.waitKey()

            if download_path:
                cv2.imwrite(download_path, det_img)

        return dets
