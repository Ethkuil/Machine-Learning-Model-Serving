from flask import request, jsonify
from werkzeug.utils import secure_filename
from app import app, data
import datetime
import os
import base64
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
        } for i in data.modelList]
        return_response = {"data": responseData}
        return jsonify(return_response)

    elif request.method == 'POST':
        modelArgs = request.values.to_dict()

        file = request.files.get('file')
        if file is None:
            return jsonify({"error": "参数不正确"})
        fileName = secure_filename(file.filename).replace(" ", "")
        filePath = f'{os.path.dirname(__file__)}/upload/{data.dataIndex}.{fileExtension(fileName)}'
        file.save(filePath)

        input, target = readModel(filePath)
        inputVariables = []
        for ii in input:
            inputVars = {
                "field": ii.name,
                "data_type": ii.dataType,
                "op_type": ii.opType
            }
            inputVariables.append(inputVars)
        targetVariables = []
        for ii in target:
            targetVars = {
                "field": ii.name,
                "data_type": ii.dataType,
                "op_type": ii.opType
            }
            targetVariables.append(targetVars)

        mymodel = data.myModel(data.dataIndex, modelArgs['name'],
                               modelArgs['description'], modelArgs['type'],
                               filePath, datetime.datetime.now())
        data.dataIndex += 1
        data.addModel(mymodel)

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


@app.route('/models/<int:id>/predict', methods=['POST'])
def modelPredict(id):
    # 获取模型
    try:
        mymodel = data.getModel(id)
        if mymodel is None:
            raise Exception("模型不存在")
    except Exception as e:
        response = jsonify({"error": str(e)})
        response.status_code = 404
        return response
    filePath = mymodel.filePath

    # 读取body，获取输入数据
    inputData = {}
    if request.headers.get('Content-Type') == 'multipart/form-data':
        for key in request.files:
            inputData[key] = request.files[key]
        for key in request.form:
            inputData[key] = request.form[key]
    elif request.headers.get('Content-Type') == 'application/json':
        body = request.json
        for key in body:
            if isinstance(body[key], dict) and body[key]['type'] == 'base64':
                inputData[key] = base64.b64decode(body[key]['value'])
            else:
                inputData[key] = body[key]

    # 利用模型预测
    result = predict(modelFilePath=filePath, type=mymodel.type, data=inputData)
    # 化为json格式
    result = {key: result[key] for key in result}

    responseData = {
        "data": {
            "result": result
        }
    }
    return jsonify(responseData)
