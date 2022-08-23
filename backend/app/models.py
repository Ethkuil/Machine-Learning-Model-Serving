from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
import base64
from app import app
from .data import MODELS
from .utils.readModel import readModel
from .utils.utils import fileExtension
from .utils.predict import predict


@app.route('/models', methods=['POST', 'GET'])
def models():
    if request.method == 'GET':
        responseData = [{
            "id": i.id,
            "name": i.name,
            "type": i.type,
            "update_time": i.updateTime
        } for i in MODELS.getModels()]
        return_response = {"data": responseData}
        return jsonify(return_response)

    elif request.method == 'POST':
        modelArgs = request.values.to_dict()

        file = request.files.get('file')
        if not file:
            return jsonify({"error": "no file"}), 400
        fileName = secure_filename(file.filename).replace(" ", "")
        filePath = f'{os.path.dirname(__file__)}/upload/{MODELS.nextId}.{fileExtension(fileName)}'
        file.save(filePath)

        try:
            input, target, algorithm = readModel(filePath)
        except Exception as e:
            os.remove(filePath)
            return jsonify({"error": f"model not valid: {e}"}), 400

        inputVariables = [{
            "field": ii.name,
            "data_type": ii.dataType,
            "op_type": ii.opType,
            "shape": ii.shape or "",
            "value": ii.value or ""
        } for ii in input]

        targetVariables = [{
            "field": ii.name,
            "data_type": ii.dataType,
            "op_type": ii.opType,
            "shape": ii.shape or "",
            "value": ii.value or ""
        } for ii in target]

        mymodel = MODELS.addModel(modelArgs['name'], modelArgs['description'],
                                  modelArgs['type'], filePath)

        return_response = {
            "data": {
                "id": mymodel.id,
                "name": mymodel.name,
                "type": mymodel.type,
                "update_time": mymodel.updateTime,
                "description": mymodel.description,
                "input_variables": inputVariables,
                "target_variables": targetVariables
            }
        }
        return jsonify(return_response)


@app.route('/models/<int:id>', methods=['GET', 'DELETE'])
def someModel(id):
    if request.method == 'DELETE':
        try:
            if MODELS.deleteModel(id):
                return jsonify({"data": "success"})
            else:
                return jsonify({"error": "model not found"}), 404
        except IndexError:
            return jsonify({"error": "model not found"}), 404

    elif request.method == 'GET':
        try:
            model = MODELS.getModel(id)
            if not model:
                return jsonify({"error": "model not found"}), 404
        except IndexError:
            return jsonify({"error": "model not found"}), 404
        inputs, target, algorithm = readModel(model.filePath)
        inputVariables = []
        targetVariables = []
        for ii in inputs:
            inputVars = {
                "field": ii.name,
                "data_type": ii.dataType,
                "op_type": ii.opType,
                "shape": ii.shape,
                "value": ii.value
            }
            inputVariables.append(inputVars)
        for ii in target:
            targetVars = {
                "field": ii.name,
                "data_type": ii.dataType,
                "op_type": ii.opType,
                "shape": ii.shape,
                "value": ii.value
            }
            targetVariables.append(targetVars)
        response = {
            "id": model.id,
            'name': model.name,
            'type': model.type,
            "update_time": model.updateTime,
            'description': model.description,
            "input_variables": inputVariables,
            "target_variables": targetVariables,
            "services": model.services,
        }
        return jsonify({'data': response})


@app.route('/models/<int:id>/predict', methods=['POST'])
def modelPredict(id):
    # 获取模型
    try:
        mymodel = MODELS.getModel(id)
        if not mymodel:
            return jsonify({"error": "model not found"}), 404
    except Exception:
        return jsonify({"error": "model not found"}), 404
    filePath = mymodel.filePath

    # 读取body，获取输入数据
    inputData = {}
    if 'multipart/form-data' in request.content_type:
        # 将字符串转换为Python数据类型
        # 合并表单和文件
        inputData = {
            **{key: eval(value)
               for key, value in request.form.items()},
            **request.files
        }
    elif request.content_type == "application/json":
        body = request.json
        for key in body:
            if isinstance(body[key], dict) and body[key]['type'] == 'base64':
                inputData[key] = base64.b64decode(body[key]['value'])
            else:
                inputData[key] = body[key]

    # 利用模型预测
    result = predict(modelFilePath=filePath, type=mymodel.type, data=inputData)

    responseData = {"data": {"result": result}}
    return jsonify(responseData)
