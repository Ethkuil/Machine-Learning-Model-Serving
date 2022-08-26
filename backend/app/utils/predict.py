# 利用已有模型预测

import pypmml
import onnxruntime as rt
import numpy as np
import pandas as pd
import io
import zipfile
from app.utils.utils import fileExtension, fileToTensorRaw, readCSV


def predict(modelFilePath: str, type: str, data: dict):
    """
    一次性预测

    :return: 预测结果，dict类型
    """
    if type.upper() == 'PMML':
        model = pypmml.Model.fromFile(modelFilePath)
        return predictPMML(model, data)
    elif type.upper() == 'ONNX':
        session = rt.InferenceSession(modelFilePath)
        return predictONNX(session, data)


def predictPMML(model, data: dict):
    result = model.predict(data)
    result = {key: result[key] for key in result}  # 转化为字典
    return result


def predictONNX(session, data: dict):
    output_names = [x.name for x in session.get_outputs()]
    result = session.run(output_names, data)
    # 将result中的数据转化为标准Python数据类型
    for i in range(len(result)):
        if isinstance(result[i], np.ndarray):
            result[i] = result[i].tolist()
    # 转化为字典
    result = dict(zip(output_names, result))
    return result


def predictDataset(modelFilePath: str, type: str, datasetFilePath: str):
    """
    预测数据集

    :return: 结果数据集文件路径
    """
    if type.upper() == 'PMML':
        model = pypmml.Model.fromFile(modelFilePath)
        if fileExtension(datasetFilePath) == 'csv':
            data = pd.read_csv(datasetFilePath)
            result = model.predict(data)
            resultFilePath = datasetFilePath.replace('.csv', '_result.csv')
            result.to_csv(resultFilePath, index=False),
            return resultFilePath

    elif type.upper() == 'ONNX':
        session = rt.InferenceSession(modelFilePath)
        if fileExtension(datasetFilePath) == 'csv':
            results = [
                predictONNX(session, data) for data in readCSV(datasetFilePath)
            ]
            resultFilePath = datasetFilePath.replace('.csv', '_result.csv')
            # 将结果数据集写入csv文件
            with open(resultFilePath, 'w') as f:
                f.write(','.join(results[0].keys()) + '\n')
                for result in results:
                    f.write(','.join([str(value)
                                      for value in result.values()]) + '\n')
            return resultFilePath
        elif fileExtension(datasetFilePath) == 'zip':
            # 获取输入变量名
            input_names = [x.name for x in session.get_inputs()]
            results = []
            with zipfile.ZipFile(io.BytesIO(
                    open(datasetFilePath, 'rb').read())) as zip:
                # 遍历zip文件中的文件，并预测
                for file in zip.namelist():
                    if fileExtension(file) == 'png':
                        # result的第1列，用于存储输入图片名
                        result = {"input_file": file}
                        with zip.open(file, 'r') as f:
                            data = {
                                input_name: fileToTensorRaw('png', f)
                                for input_name in input_names
                            }
                        result |= predictONNX(session, data)
                        results.append(result)
                # 将结果数据集写入csv文件
            resultFilePath = datasetFilePath.replace('.zip', '_result.csv')
            with open(resultFilePath, 'w') as f:
                f.write(','.join(results[0].keys()) + '\n')
                for result in results:
                    f.write(','.join([str(value)
                                      for value in result.values()]) + '\n')
            return resultFilePath
