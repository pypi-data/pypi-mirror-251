import os
from pathlib import Path

from PIL import Image
import torch
import torch.backends.cudnn as cudnn
from numpy import random

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages
from utils.general import (
    check_img_size, non_max_suppression, apply_classifier, scale_coords, xyxy2xywh, plot_one_box, strip_optimizer)
from utils.torch_utils import select_device, load_classifier, time_synchronized
from crop import crop

class FaceCrop:
    def __init__(self):
        self.device = select_device()
        self.half = self.device.type != 'cpu'

    def load_dataset(self, source):
        self.source = source
        self.dataset = LoadImages(source)
        print(f'Successfully load dataset from {source}')
    
    def load_model(self, model=None):
        if model == None:
            self.model = attempt_load('FaceCropAnime/yolov5x_anime.pt', map_location=self.device)
        else:
            raise RuntimeError('Customized Models are not supported.')
        if self.half:
            self.model.half()
        print(f'Successfully load model weights from {model}')
    
    def set_crop_config(self, out_folder, target_size, mode=0, face_ratio=3, threshold=1.5):
        self.out_folder = out_folder
        self.target_size = target_size
        self.mode = mode
        self.face_ratio = face_ratio
        self.threshold = threshold
    
    def info(self):
        attributes = dir(self)
        for attribute in attributes:
            if not attribute.startswith('__') and not callable(getattr(self, attribute)):
                value = getattr(self, attribute)
                print(attribute, " = ", value)
    
    def process(self):
        for path, img, im0s, vid_cap in self.dataset:
            img = torch.from_numpy(img).to(self.device)
            img = img.half() if self.half else img.float()  # uint8 to fp16/32
            img /= 255.0  # 0 - 255 to 0.0 - 1.0
            if img.ndimension() == 3:
                img = img.unsqueeze(0)

            # Inference
            pred = self.model(img, augment=False)[0]

            # Apply NMS
            pred = non_max_suppression(pred)

            # Process detections
            for i, det in enumerate(pred):  # detections per image

                p, s, im0 = path, '', im0s

                in_path = str(Path(self.source) / Path(p).name)
                
                #txt_path = str(Path(out) / Path(p).stem)
                s += '%gx%g ' % img.shape[2:]  # print string
                gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh

                if det is not None and len(det):
                    # Rescale boxes from img_size to im0 size
                    det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                    # Write results
                    ind = 0
                    for *xyxy, conf, cls in det:
                        if conf > 0.6:  # Write to file
                            out_path = os.path.join(str(Path(self.out_folder)), Path(p).name.replace('.', '_'+str(ind)+'.'))
                            ind += 1
                            x, y, w, h = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()
                            crop(in_path, (x, y), out_path, mode=self.mode, size=self.target_size, box=(w, h), face_ratio=self.face_ratio, shreshold=self.threshold)
                print(f'Successfully cropped and saved as {out_path}')



    