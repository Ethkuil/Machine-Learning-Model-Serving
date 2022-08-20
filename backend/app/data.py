
#存放各类数据 列表存入的是绝对路径
# id从 0 开始

import datetime, os

class Model:
    def __init__(self,id,name,description,_type,filepath,updateTime):
        self.id=id
        self.name=name
        self.description=description
        self.type=_type
        self.filepath=filepath
        self.updateTime=updateTime

class Models:
    def __init__(self):
        self.__models = []
        self.nextId = 0
        
    def addModel(self, name, description, _type, filepath):
        newModel = Model(self.nextId, name, description, _type, filepath, datetime.datetime.now())
        self.__models.append(newModel)
        self.nextId += 1
        return newModel.id

    def findModel(self , id):  #根据picked寻找对应的model，返回值为model
        return self.__models[id]

    def deleteModel(self, id):
        model = self.__models[id]
        if model:
            os.remove(model.filepath)
            self.__models[id] = None
            return True
        else:
            return False
    
    def getNextId(self):
        return self.nextId   
    
def dataInit():
    global MODELS
    MODELS = Models()