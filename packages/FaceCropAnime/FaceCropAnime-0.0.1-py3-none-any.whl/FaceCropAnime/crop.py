import os
from pathlib import Path
from PIL import Image

def crop(image_path, point, output_path, mode=0, size=(512, 512), box=None, face_ratio=3, shreshold=1.5):
    img = Image.open(image_path)
    img_width, img_height = img.size
    tgt_width, tgt_height = size
    point = (point[0]*img_width, point[1]*img_height)

    # mode 0 : automatic
    if mode == 0:
        if box is None:
            raise RuntimeError('face bax parameter expected: missing box=(width, height)')
        if img_width < tgt_width or img_height < tgt_height:
            mode = 1
        elif face_ratio ** 2 * shreshold ** 2 * box[0] * box[1] * img_width * img_height < tgt_width * tgt_height:
            mode = 2
        else:
            mode = 3

    # mode 1 : no scale
    if mode == 1:
        pass

    # mode 2 : full screen - crop as largr as possible
    if mode == 2:
        if tgt_width/img_width > tgt_height/img_height:
            r = tgt_height / tgt_width
            tgt_width = img_width
            tgt_height = round(tgt_width * r)
        else:
            r = tgt_width / tgt_height
            tgt_height = img_height
            tgt_width = round(tgt_height * r)  
    
    # mode 3 : fixed face ratio
    if mode == 3:
        if box is None:
            raise RuntimeError('face bax parameter expected: missing box=(width, height)')
        box_width = box[0] * img_height
        box_height = box[1] * img_height
        if box_width/tgt_width > box_height/tgt_width:
            r = tgt_height / tgt_width
            tgt_width = box_width * face_ratio
            tgt_height = round(tgt_width * r)
        else:
            r = tgt_width / tgt_height
            tgt_height = box_height * face_ratio
            tgt_width = round(tgt_height * r) 


    # upscale raw image if target size is over raw image size
    if img_width < tgt_width or img_height < tgt_height:
        if img_width < img_height:
            img_height = round(tgt_width * img_height / img_width)
            img_width = tgt_width
            img = img.resize((img_width, img_height))
        else:
            img_width = round(tgt_height * img_width / img_height)
            img_height = tgt_height
            img = img.resize((img_width, img_height)) 

    left = point[0] - tgt_width // 2
    top = point[1] - tgt_height // 2
    right = point[0] + tgt_width // 2
    bottom = point[1] + tgt_height // 2

    if left < 0:
        right -= left
        left = 0
    if right > img_width:
        left -= (right-img_width)
        right = img_width
    if top < 0:
        bottom -= top
        top = 0
    if bottom > img_height:
        top -= (bottom-img_height)
        bottom = img_height

    cropped_img = img.crop((left, top, right, bottom))
    cropped_img = cropped_img.resize(size)
    cropped_img.save(output_path)
