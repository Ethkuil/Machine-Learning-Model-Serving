from urllib import response
from flask import request, jsonify
from werkzeug.utils import secure_filename
import datetime, os
from app import app
import base64
from utils.readModel import readModel
from utils.utils import fileExtension
from utils.predict import predict
from data import MODELS

'''
export FLASK_APP=models.py
python3 -m flask run
'''

@app.route('/models', methods=['POST', 'GET'])
def models():
    if request.method == 'GET':
        responseData = []
        for i in range(MODELS.getNextId()):
            _model = MODELS.findModel(i)
            if _model is None: # 如果i被删除了
                pass
            else:
                responseData.append({
                    "id": _model.id,
                    "name": _model.name,
                    "type": _model.type,
                    "update_time": _model.updateTime
                })
        return_response = {"data": responseData}
        return jsonify(return_response)

    elif request.method == 'POST':
        modelArgs = request.values.to_dict()
        file = request.files.get('file')
        if file is None:
            return jsonify({"error": "参数不正确"})
        fileName = secure_filename(file.filename).replace(" ", "")
        filePath = f'{os.path.dirname(__file__)}/upload/{MODELS.getNextId()}.{fileExtension(fileName)}'
        file.save(filePath)
        input, target, algorithm = readModel(filePath)
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

        MODELS.addModel(modelArgs['name'],
                               modelArgs['description'], modelArgs['type'],
                               filePath)

        return_response = {
            "data": {
                "id": MODELS.getNextId() - 1,
                "name": modelArgs['name'],
                "type": modelArgs['type'],
                "update_time": datetime.datetime.now(),
                "description": modelArgs['description'],
                "input_variables": inputVariables,
                "target_variables": targetVariables
            }
        }
        return jsonify(return_response)

@app.route('/models/<int:id>', methods=['POST', 'GET', 'DELETE'])
def someModel(id): 
    if request.method=='DELETE':
        if MODELS.deleteModel(id):
            return jsonify({'status': 'success'})
        else:
            return "no File", 404
        
    # elif method == GET   Model Detail 启动时
    model = MODELS.findModel(id) #找到当前的模型
    inputs, target, algorithm = readModel(model.filepath)
    inputVariables=[]
    targetVariables=[]
    for ii in inputs:
        inputVars={
            "field":ii.name,
            "data_type":ii.dataType,
            "op_type":ii.opType,
            "shape":ii.shape,
            "value":ii.value
        }
        inputVariables.append(inputVars)  
    for ii in target:
        targetVars={
            "field":ii.name,
            "data_type":ii.dataType,
            "op_type":ii.opType,
            "shape":ii.shape,
            "value":ii.value
        }
        targetVariables.append(targetVars)           
    response = {
        # 'filePath': filePathStr,
        "id": model.id,
        "update_time": model.updateTime,
        'name': model.name,
        'type': model.type,
        'description': model.description,
        "input_variables":inputVariables,
        "target_variables":targetVariables,
        "service":""
    }
    return jsonify({'data': response})

@app.route('/models/<int:id>/predict', methods=['POST'])
def modelPredict(id):
    # 获取模型
    try:
        mymodel = MODELS.findModel(id)
        if mymodel is None:
            raise Exception("模型不存在")
    except Exception as e:
        response = jsonify({"error": str(e)})
        response.status_code = 404
        return response
    filePath = mymodel.filepath

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