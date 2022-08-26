from flask import request, jsonify

from threading import Thread
import base64

from app import app
from app.data import SERVICES, MODELS
from app.deploy.services import deployService

from app.utils.predict import predict
from app.utils.utils import fileToTensor, fileToTensorRaw


@app.route('/services', methods=['POST', 'GET'])
def services():
    if request.method == 'GET':
        responseData = [{
            'id': service.id,
            'name': service.name,
            'start_time': service.startTime,
            'state': service.state,
        } for service in SERVICES.getServices()]
        return jsonify({'data': responseData})
    elif request.method == 'POST':
        try:
            body = request.json
            name = body['name']
            modelId = body['model_id']

            model = MODELS.getModel(modelId)
            service = SERVICES.addService(name, modelId)

            # 新开1个线程执行任务
            Thread(target=deployService,
                   args=(service.id, model.filePath)).start()

            return jsonify({
                "data": {
                    "id": service.id,
                    "name": service.name,
                    "start_time": service.startTime,
                    "state": service.state,
                    "model": {
                        "id": model.id,
                        "name": model.name,
                        "type": model.type,
                        "update_time": model.updateTime,
                    }
                }
            })
        except IndexError:
            return jsonify({"error": "model not found"}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400


@app.route('/services/<int:id>', methods=['GET', 'DELETE'])
def service(id):
    if request.method == 'GET':
        try:
            service = SERVICES.getService(id)
            if not service:
                return jsonify({"error": "service not found"}), 404
        except IndexError:
            return jsonify({"error": "service not found"}), 404
        model = MODELS.getModel(service.modelId)
        responseData = {
            'id': service.id,
            'name': service.name,
            'start_time': service.startTime,
            'state': service.state,
            'model': {
                'id': model.id,
                'name': model.name,
                'type': model.type,
                'update_time': model.updateTime,
            }
        }
        return jsonify({'data': responseData})
    elif request.method == 'DELETE':
        try:
            return jsonify({"data": "success"
                            }) if SERVICES.deleteService(id) else (jsonify(
                                {"error": "service not found"}), 404)
        except IndexError:
            return jsonify({"error": "service not found"}), 404


@app.route('/services/<int:id>/start', methods=['POST'])
def service_start(id):
    try:
        return jsonify({"data": "success"}) if SERVICES.updateService(
            id, "运行中") else (jsonify({"error": "service not found"}), 404)
    except IndexError:
        return jsonify({"error": "service not found"}), 404


@app.route('/services/<int:id>/pause', methods=['POST'])
def service_pause(id):
    try:
        return jsonify({"data": "success"}) if SERVICES.updateService(
            id, "暂停中") else (jsonify({"error": "service not found"}), 404)
    except IndexError:
        return jsonify({"error": "service not found"}), 404


@app.route('/services/<int:id>/predict', methods=['POST'])
def service_predict(id):
    try:
        service = SERVICES.getService(id)
        if not service:
            return jsonify({"error": "service not found"}), 404
    except IndexError:
        return jsonify({"error": "service not found"}), 404
    if service.state != '运行中':
        return jsonify({"error": "service not running"}), 400

    # 获取模型
    model = MODELS.getModel(service.modelId)

    # 读取body，获取输入数据
    inputData = {}
    if 'multipart/form-data' in request.content_type:
        # 合并表单和文件
        inputData = {
            key: eval(value)  # 将字符串转换为供预测用的值
            for key, value in request.form.items()
        } | {
            key: fileToTensor(file)  # 将文件转换为供预测用的值
            for key, file in request.files.items()
        }
    elif request.content_type == "application/json":
        body = request.json
        for key in body:
            if isinstance(body[key], dict) and body[key]['type'] == 'base64':
                inputData[key] = fileToTensorRaw(
                    'png', base64.b64decode(body[key]['value']))
            else:
                inputData[key] = body[key]

    # 利用模型预测
    result = predict(modelFilePath=model.filePath,
                     type=model.type,
                     data=inputData)

    responseData = {"data": {"result": result}}
    return jsonify(responseData)
