from app.data import SERVICES, MODELS
from app.utils.predict import predict

def deployService(serviceId, modelId):
    # 运行中
    SERVICES.updateService(serviceId, state='运行中')

    return True

