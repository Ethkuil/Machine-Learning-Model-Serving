import re
# testStr = 'mnist-8.onnx'#'rf_iris.onnx'#'.\demo.pmml'#'xgb-iris.pmml'# 'models/randomForest.pmml'  # get from front end


class dataElement():

    def __init__(self, name="", dataType="", opType="", shape=""):
        self.name = name  #字段
        self.dataType = dataType  #类型
        self.opType = opType  #测量
        self.value = []  #取值
        self.shape = shape


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
    # print(miningSchema)
    datafield = dataDict.split("<DataField ")
    del datafield[0]

    #print(datafield)

    yIndex = []

    # to do: find "usageType="target" --> mark its index --> add to y
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

        print(name, "  ", opType, "  ", dataType)
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
                print(newDataElement.value)
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
        print(modelName)
        model = model.split('functionName=\"')[1]
        model = model[:-1]
    modelType = modelName +'(' + model + ')'
    print(modelType)
    return x, y, modelType
    


def readONNX(openFileStr):
    x.clear()
    y.clear()
    import onnx
    import onnxruntime
    onnx_model = onnx.load(openFileStr)
    onnxSession = onnxruntime.InferenceSession(openFileStr)
    for node in onnxSession.get_inputs():
        newElement = dataElement(node.name, node.type, "", str(node.shape))
        print(node.name, " ", node.type, " ", str(node.shape))
        newElement.value = ''
        x.append(newElement)

    for node in onnxSession.get_outputs():
        newElement = dataElement(name=node.name, dataType=node.type, shape=str(node.shape) if str(node.shape) != '[]' else '')
        print(node.name," ", node.type, " ", str(node.shape) if str(node.shape) != '[]' else '')
        newElement.value = ''
        y.append(newElement)

    # Check the model
    try:
        onnx.checker.check_model(onnx_model)
    except onnx.checker.ValidationError as e:
        print('The model is invalid: %s' % e)
    else:
        print('The model is valid!')
        
    return x, y, '-'
    '''
    # iterate through inputs of the graph
    for input in onnx_model.graph.input:
        print (input.name, end=": ")
        # get type of input tensor
        tensor_type = input.type.tensor_type
        # check if it has a shape:
        if (tensor_type.HasField("shape")):
            # iterate through dimensions of the shape:
            for d in tensor_type.shape.dim:
                # the dimension may have a definite (integer) value or a symbolic identifier or neither:
                if (d.HasField("dim_value")):
                    print (d.dim_value, end=", ")  # known dimension
                elif (d.HasField("dim_param")):
                    print (d.dim_param, end=", ")  # unknown dimension with symbolic name
                else:
                    print ("?", end=", ")  # unknown dimension with no name
        else:
            print ("unknown rank", end="")
        print()
    '''
    #output = onnx_model.graph.output
    #print(output)


''''''

# to do: 判断是pmml类型还是onnx类型


# to do: 验证pmml文件有效性
def readModel(openFileStr):
    if openFileStr[-5:] == '.pmml':
        return readPMML(openFileStr)
        '''for xx in x:
            print('x: ', xx.name)
        for yy in y:
            print('y: ', yy.name)'''
    elif openFileStr[-5:] == ".onnx":
        return readONNX(openFileStr)
        '''for xx in x:
            print('x: ', xx.name)
        for yy in y:
            print('y: ', yy.name)'''
    else:
        print("wrong input file!")
        exit(0)
    return x, y, '-'
