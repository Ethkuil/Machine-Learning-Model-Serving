from app.data import JOBS, MODELS
from app.utils.predict import predictDataset


def deployJob(jobId, datasetFilePath):
    # 运行中
    JOBS.updateJob(jobId, state='运行中')
    model = MODELS.getModel(JOBS.getJob(jobId).modelId)
    modelFilePath = model.filePath
    modelType = model.type
    resultFilePath = predictDataset(modelFilePath, modelType, datasetFilePath)

    # 成功
    JOBS.updateJob(jobId, state='成功', resultFilePath=resultFilePath)
