#存放各类数据 列表存入的是绝对路径



class myModel:
    def __init__(self,id,name,description,type,filepath,updateTime):
        self.id=id
        self.name=name
        self.description=description
        self.type=type
        self.filepath=filepath
        self.updateTime=updateTime
    
    
def dataInit():
    global modelList
    global dataIndex
    dataIndex=0
    modelList=[]
    
    
def addModel(model):
    global modelList
    modelList.append(model)
    return len(modelList)-1