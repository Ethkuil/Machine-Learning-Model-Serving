import base64
from io import BytesIO

from flask import Request

from app.utils.utils import fileToTensor, fileToTensorRaw


def mergeFormDataAndFile(request: Request):
    """
    对表单和文件数据各自处理后，合并为一个字典
    """
    return {
        # 将字符串转换为供预测用的值
        key: eval(value)
        for key, value in request.form.items()
    } | {
        # 将文件转换为供预测用的值
        key: fileToTensor(file)
        for key, file in request.files.items()
    }


def base64ToTensor(b64_str: str):
    """
    将base64编码的图片转换为tensor
    """
    imageData = base64.b64decode(b64_str)
    return fileToTensorRaw('png', BytesIO(imageData))
