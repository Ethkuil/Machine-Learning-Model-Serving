# 利用已有模型预测

import onnx
import onnxruntime
import numpy as np
import json, re
from .readModel import readModel
import pypmml

def predict(modelFilePath: str, type: str, data):  # data是输入变量的dict
    if type.upper() == 'PMML':
        return testPMML(modelFilePath, data)
    elif type.upper() == 'ONNX':
        return testONNX(modelFilePath, data)
    
       
def testPMML(filepath, data):
    model = pypmml.Model.fromFile(filepath)
    X_in, y_in, al = readModel(filepath)
    X_test = []
    for i in X_in:
        if i.dataType == 'double' or i.dataType == 'float':
            X_test.append(float(data[i.name]))
        elif i.dataType == 'int':
            X_test.append(int(data[i.name]))
    res = model.predict(X_test)
    outputList = searchOutput(filepath)  # 输出变量名称列表
    outputDict = dict()
    for i in range(len(res)):
        print(outputList[i], ' ', res[i])
        outputDict[outputList[i]] = res[i]
    return outputDict
    
    
'''   line73~78
    <Output>
            <OutputField name="probability_0" optype="continuous" dataType="double" feature="probability" value="0"/>
            <OutputField name="probability_1" optype="continuous" dataType="double" feature="probability" value="1"/>
            <OutputField name="probability_2" optype="continuous" dataType="double" feature="probability" value="2"/>
            <OutputField name="predicted_Species" optype="categorical" dataType="integer" feature="predictedValue"/>
        </Output>
'''
def searchOutput(filepath):
    pmmlFile = open(filepath)# open('xgb-iris.pmml') # open('.\demo.pmml')
    codes = pmmlFile.read()
    output = re.search(r"\<Output\>(\s|\S)*\</Output\>", codes)
    output = output.group()
    outputField = output.split('<OutputField')
    outputList = []
    del outputField[0]
    i = 0
    for eachElement in outputField:
        name = re.search(r"name=\"(\S|\s)+\"", eachElement)
        if name is not None:
            name = name.group()
            name = name.split("\"")[1]
        print(name)
        outputList.append(name)
    return outputList
        
def testONNX(filepath, data):
    model = onnx.load(filepath)
    ort_session = onnxruntime.InferenceSession(model.SerializeToString())
    ort_inputs = {}
    # print(data)
    for i, input_ele in enumerate(ort_session.get_inputs()):
        # print('data: ', data[input_ele.name])
        #检查输入类型
        if 'tensor' in input_ele.type: # 如果是tensor类型变量
            # 用正则匹配找到字符串中所有数字，返回值为list 
            nums = getNums(data[input_ele.name])
            # 再将list转为np.array
            if 'float' in input_ele.type: # 如果是tensor(float)类型变量
                inputValue = np.array([nums]).astype(np.float32)  
                # print(inputValue)           
            elif 'double' in input_ele.type: 
                inputValue = np.array(nums).astype(np.float32)
            # 最后reshape得到符合input维度的tensor   
            inputValue = inputValue.reshape(input_ele.shape)
            print('input_ele.shape: ', inputValue.shape)
            # 好像只能这样强行把字符串转换为numpy
            ort_inputs[input_ele.name] = inputValue
    outputs = [x.name for x in ort_session.get_outputs()]
    ort_outs = ort_session.run(outputs, ort_inputs)
    outputDict = dict()
    for i, output_ele in enumerate(ort_session.get_outputs()):
        if type(ort_outs[i]) == type(np.array([])): # 糊弄
            print(type(ort_outs[i]))
            outputDict[output_ele.name] = np.ndarray.tolist(ort_outs[i])
        else:
            outputDict[output_ele.name] = ort_outs[i]
    return outputDict# "upload/testResult.json"

'''tmp = data[input_ele.name][2:-2]
            tmp = tmp.split(',')
            nums = []
            for el in tmp:
                nums.append(float(el))'''

def getNums(string):
    ret = []
    find = re.findall(r"-?[1-9]\d*\.\d*(?#绝对值大于1的浮点数)|-?0\.\d*(?#绝对值小于1的浮点数)|-?\d+(?#整数)", string)
    print(find)
    for f in find:
        ret.append(float(f))
    return ret

def toJSONoutput(res):
    out = dict()
    out['result'] = res
    out['stderr'] = []  # 糊弄哈哈哈哈哈 (我也不知道这部分什么意思)
    out['stdout'] = []
    return out