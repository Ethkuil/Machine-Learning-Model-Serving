import pandas as pd
import numpy as np
from PIL import Image


def fileExtension(fileName):
    return fileName.rsplit('.', 1)[1].lower()


def readCSV(filePath: str):
    """
    读取csv文件，返回字典列表
    """
    data = pd.read_csv(filePath)
    # 表头为输入变量名
    inputNames = data.columns.tolist()
    # 剩余行为输入数据，1行1份数据
    inputData = data.values.tolist()

    # 将输入数据转化为字典
    # 若带有引号，则使用eval函数转化为Python数据类型
    return [{
        inputNames[i]: (eval(inputData[j][i]) if isinstance(
            inputData[j][i], str) else inputData[j][i])
        for i in range(len(inputNames))
    } for j in range(len(inputData))]


def fileToTensor(file: object):
    """
    将文件转化为tensor，用于预测

    :param file: Flask file对象
    """
    fileType = fileExtension(file.filename)
    fileToTensor(fileType, file.stream)


def fileToTensor(fileType, file:object):
    """
    将文件转化为tensor，用于预测

    :param file: 必须实现了file.read()方法
    """
    # 检测文件类型
    if fileType == 'png':
        image = Image.open(file)
        # 调整图片大小
        image.resize((28, 28))
        # 转化为灰度图
        image = image.convert('L')
        # 归一化
        image = np.array(image).astype(np.float32) / 255.0
        # 将图片转化为tensor
        image = image.reshape((1, 1, 28, 28))
        return image
