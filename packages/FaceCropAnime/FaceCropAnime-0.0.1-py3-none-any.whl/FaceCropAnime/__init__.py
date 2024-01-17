import sys
import os

sys.path[0] = os.path.join(sys.path[0], 'FaceCropAnime')

from face_crop import FaceCrop
'''
# download fine-tuned yolo model
import urllib.request

if not os.path.exists("yolov5x_anime.pt"):
    print('downloading model weights from https://github.com/Carzit/FaceCropAnime-Pipeline/releases/download/Model_Weights/yolov5x_anime.pt')
    url = "https://github.com/Carzit/FaceCropAnime-Pipeline/releases/download/Model_Weights/yolov5x_anime.pt"  # 给定的下载链接
    urllib.request.urlretrieve(url, "yolov5x_anime.pt")  # 下载并保存为1.jpg文件
    print("download successfully")

'''



__all__= ['FaceCropAnime', 'FaceCrop']