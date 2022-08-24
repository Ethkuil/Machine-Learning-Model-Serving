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
        self.jobs = []


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


class Job:

    def __init__(
        self,
        id,
        name,
        startTime,
        state,
        modelId,
        resultFilePath,
    ):
        self.id = id
        self.name = name
        self.startTime = startTime
        self.state = state
        self.modelId = modelId
        self.resultFilePath = resultFilePath


class Jobs:

    def __init__(self):
        self.__jobs = []
        self.nextId = 0

    def getJob(self, id):
        return self.__jobs[id]

    def getJobs(self):
        return [i for i in self.__jobs if i]

    def addJob(self, name, modelId):
        """
        :return: 所添加的任务变量
        """
        job = Job(self.nextId, name, datetime.datetime.now(), "启动中", modelId,
                  None)
        self.nextId += 1
        self.__jobs.append(job)
        return job

    def deleteJob(self, id):
        """
        :return: True, 若正确删除；False, 若任务不存在
        """
        if job := self.__jobs[id]:
            self.__jobs[id] = None
            return True
        else:
            return False

    def updateJob(self, id, state=None, resultFilePath=None):
        """
        :param resultFilePath: 当state为"成功"时，resultFilePath为结果文件的路径
        :return: True, 若正确更新；False, 若任务不存在
        """
        if job := self.__jobs[id]:
            if state: job.state = state
            job.resultFilePath = resultFilePath if resultFilePath and state == "成功" else None
            return True
        else:
            return False

    def deleteJobs(self, id):
        """
        :return: True, 若正确删除；False, 若任务不存在
        """
        if job := self.__jobs[id]:
            self.__jobs[id] = None
            return True
        else:
            return False

    def deleteJobs(self):
        self.__jobs = []


def dataInit():
    # 全局变量命名规范：全大写，下划线分割
    global MODELS
    MODELS = Models()
    global JOBS
    JOBS = Jobs()
