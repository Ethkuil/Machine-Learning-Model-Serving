import re
from app.utils.utils import fileExtension

class dataElement():

    def __init__(self, name="", dataType="", opType="", shape=""):
        self.name = name  #字段
        self.dataType = dataType  #类型
        self.opType = opType  #测量
        self.value = []  #取值
        self.shape = shape  #维度


x = []
y = []


def readPMML(openFileStr):
    x.clear()
    y.clear()
    pmmlFile = open(openFileStr)  # open('xgb-iris.pmml') # open('.\demo.pmml')
    codes = pmmlFile.read()
    dataDict = re.search(
        r"\<DataDictionary((\snumberOfFields=\"\d+\")?)\>(\s|\S)*\</DataDictionary\>",
        codes)
    dataDict = dataDict.group()
    miningSchema = re.search(r"\<MiningSchema(\s|\S)*?\</MiningSchema", codes)
    miningSchema = miningSchema.group()
    datafield = dataDict.split("<DataField ")
    del datafield[0]

    yIndex = []

    miningSchema = miningSchema.split("<MiningField ")
    del miningSchema[0]
    count = 0
    for eachElement in miningSchema:
        if "usageType=\"target\"" in eachElement or "usageType=\"predicted\"" in eachElement:
            yIndex.append(count)
        count += 1

    count = 0
    for eachElement in datafield:  # to do: 缺省值
        name = re.search(r"name=\"(\S|\s)+\"", eachElement)
        if name is not None:
            name = name.group()
            name = name.split("\"")[1]

        opType = re.search(r"optype=\"\S+\"", eachElement)
        if opType is not None:
            opType = opType.group()
            opType = opType.split("\"")[1]

        dataType = re.search(r"dataType=\"\S+\"", eachElement)
        if dataType is not None:
            dataType = dataType.group()
            dataType = dataType.split("\"")[1]

        newDataElement = dataElement(name, dataType, opType, "")
        if count in yIndex:
            y.append(newDataElement)
        else:
            x.append(newDataElement)
        if opType == 'categorical':
            pass
            # to do: find all values and add them to list value
            valueElement = eachElement.split("<Value ")
            del valueElement[0]
            for eachValue in valueElement:
                newDataElement.value.append(eachValue.split("\"")[1])
        if newDataElement.value == []:
            newDataElement.value = ""
        else:
            newDataElement.value = str(newDataElement.value)
        count += 1
    model = re.search(r"\<(\S)*?Model(\s|\S)*?functionName=\"(\s|\S)*?\"",
                      codes)
    if model is not None:
        model = model.group()
        modelName = model.split("Model")[0]
        modelName = modelName[1:] + "Model"
        model = model.split('functionName=\"')[1]
        model = model[:-1]
    modelType = modelName + '(' + model + ')'
    return x, y, modelType


def readONNX(openFileStr):
    x.clear()
    y.clear()
    import onnx
    import onnxruntime
    onnx_model = onnx.load(openFileStr)
    onnxSession = onnxruntime.InferenceSession(openFileStr)
    for node in onnxSession.get_inputs():
        newElement = dataElement(
            node.name,
            node.type,
            "",
            shape=str(node.shape) if str(node.shape) != '[]' else '')
        newElement.value = ''
        x.append(newElement)

    for node in onnxSession.get_outputs():
        newElement = dataElement(
            name=node.name,
            dataType=node.type,
            shape=str(node.shape) if str(node.shape) != '[]' else '')
        newElement.value = ''
        y.append(newElement)

    # Check the model
    onnx.checker.check_model(onnx_model)

    return x, y, '-'


# to do: 验证pmml文件有效性
def readModel(openFileStr):
    if fileExtension(openFileStr) == 'pmml':  # 支持不区分大小写
        return readPMML(openFileStr)
    elif fileExtension(openFileStr) == 'onnx':
        return readONNX(openFileStr)
    else:
        raise RuntimeError("File type is not supported")
