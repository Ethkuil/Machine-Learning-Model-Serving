#存放各类数据 列表存入的是绝对路径


class myModel:

    def __init__(self, id, name, description, type, filePath, updateTime):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.filePath = filePath
        self.updateTime = updateTime


def dataInit():
    global modelList
    global dataIndex # 用于记录新模型的id
    dataIndex = 0
    modelList = []

# 抽象为函数，不对外暴露具体实现，以便之后可能的修改
# 其他数据的操作同样建议改成这样，暴露太多细节易出错. 如dateIndex+=1本应在addModel()中自动完成
# 数据结构修改完毕后请删除这些注释
def getModel(id):
    global modelList
    return modelList[id]

def addModel(model):
    global modelList
    modelList.append(model)
    return len(modelList) - 1
