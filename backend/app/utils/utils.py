import pandas as pd
import numpy as np
from PIL import Image


def fileExtension(fileName):
    return fileName.rsplit('.', 1)[1].lower()


def fileToTensor(file):
    """
    将文件转化为tensor，用于预测
    """
    # 检测文件类型
    fileType = fileExtension(file.filename)
    if fileType == 'png':
        image = Image.open(file.stream)
        # 调整图片大小
        image.resize((28, 28))
        # 转化为灰度图
        image = image.convert('L')
        # 归一化
        image = np.array(image).astype(np.float32) / 255.0
        # 将图片转化为tensor
        image = image.reshape((1, 1, 28, 28))
        return image
