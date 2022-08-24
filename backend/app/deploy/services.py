import random
import time

from app.data import SERVICES, MODELS
from app.utils.predict import predict

def deployService(serviceId, modelPath):
    # 启动中
    # 用随机sleep时间，模拟启动时间
    time.sleep(random.uniform(1, 5))

    # 运行中
    SERVICES.updateService(serviceId, state='运行中')

    return True

