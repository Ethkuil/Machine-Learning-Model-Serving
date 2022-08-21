# 利用已有模型预测

import pypmml
import onnxruntime as rt
import numpy as np


def predict(modelFilePath: str, type: str, data):
    """
    一次性预测
    """
    if type.upper() == 'PMML':
        model = pypmml.Model.fromFile(modelFilePath)
        result = model.predict(data)
        result = {key: result[key] for key in result}  # 转化为字典
        return result
    elif type.upper() == 'ONNX':
        session = rt.InferenceSession(modelFilePath)
        output_names = [x.name for x in session.get_outputs()]
        result = session.run(output_names, data)
        # 将result中的数据转化为标准Python数据类型
        for i in range(len(result)):
            if isinstance(result[i], np.ndarray):
                result[i] = result[i].tolist()
        # 转化为字典
        result = dict(zip(output_names, result))
        return result
