# 利用已有模型预测

import pypmml
import onnxruntime as rt


def predict(modelFilePath: str, type: str, data):
    if type.upper() == 'PMML':
        model = pypmml.Model.fromFile(modelFilePath)
        return model.predict(data)
    elif type.upper() == 'ONNX':
        session = rt.InferenceSession(modelFilePath)
        return session.run(None, data)
