# 存放各类数据. 模型、服务、任务的信息
# 目前数据存放在内存中. 基本功能完成后，若有余力可使用数据库，这样重启服务器后不会丢失数据

import datetime
import os


class Model:

    def __init__(self, id, name, description, type, filePath, updateTime):
        self.id = id
        self.name = name
        self.description = description
        self.type = type
        self.filePath = filePath
        self.updateTime = updateTime
        self.services = []


class Models:

    def __init__(self):
        self.__models = []
        self.nextId = 0

    def getModel(self, id):
        return self.__models[id]

    def getModels(self):
        # 不返回空模型
        return [i for i in self.__models if i]

    def addModel(self, name, description, type, filePath):
        """
        :return: 所添加的模型变量
        """
        model = Model(self.nextId, name, description, type, filePath,
                      datetime.datetime.now())
        self.nextId += 1
        self.__models.append(model)
        return model

    def deleteModel(self, id):
        """
        :return: True, 若正确删除；False, 若模型不存在
        """
        if model := self.__models[id]:
            os.remove(model.filePath)
            self.__models[id] = None
            return True
        else:
            return False


def dataInit():
    # 全局变量命名规范：全大写，下划线分割
    global MODELS
    MODELS = Models()
