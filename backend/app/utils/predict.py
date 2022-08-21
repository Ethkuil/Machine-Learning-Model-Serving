# 利用已有模型预测

import onnx
import onnxruntime
import numpy as np
import json, re
from .readModel import readModel
import pypmml

def predict(modelFilePath: str, type: str, data):  # data是输入变量的dict
    if type.upper() == 'PMML':
        model = pypmml.Model.fromFile(modelFilePath)
        return model.predict(data)
    elif type.upper() == 'ONNX':
        return testONNX(modelFilePath, data)
    
           
def testONNX(filepath, data):
    model = onnx.load(filepath)
    ort_session = onnxruntime.InferenceSession(model.SerializeToString())
    outputs = [x.name for x in ort_session.get_outputs()]
    ort_outs = ort_session.run(outputs, data)
    return {
        output_ele.name: np.ndarray.tolist(ort_outs[i])
        if type(ort_outs[i]) == type(np.array([]))
        else ort_outs[i]
        for i, output_ele in enumerate(ort_session.get_outputs())
    }