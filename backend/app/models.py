from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
import datetime, os
import data
import base64
from utils.readModel import readModel
from utils.utils import fileExtension
from utils.predict import predict


app = Flask(__name__)
CORS(app, support_credentials=True)
# Get port number from the environment varriable
port = os.getenv("PORT")
# os.path.abspath(os.path.join(os.path.dirname("__file__"),"../.."))

data.dataInit() 

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
        filePath = f'{os.path.dirname(__file__)}/upload/{data.dataIndex + 1}.{fileExtension(fileName)}'
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

        mymodel = data.myModel(data.dataIndex + 1, modelArgs['name'],
                               modelArgs['description'], modelArgs['type'],
                               filePath, datetime.datetime.now())
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

@app.route('/models/<int:id>', methods=['POST', 'GET', 'DELETE'])
def someModel(id): 
    # 在Model Table中选中详情时
    if request.method == 'POST':
        response = {
            'url': 'success'
        }
        return jsonify(response)  
    elif request.method=='DELETE':
        findMark = False
        print('id: ', id)
        for mod in data.modelList:
            if id == mod.id:
                findMark = True
                try:
                    print('id: ', id)
                    os.remove(data.deleteModel(id))
                    return jsonify({})
                except Exception as e:
                    return jsonify({"message":{e}})
        if findMark == False:
            return "no File", 404
         
    # method == GET   Model Detail 启动时
    model = data.findModel(id) #找到当前的模型
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
        mymodel = data.findModel(id)
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
            print('key: ', key, " ", type(key))
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

if __name__ == '__main__':
    # If the app is running locally
    if port is None:
    # Use port 5000
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
    # Else use cloud foundry default port
        app.run(host='0.0.0.0', port=int(port), debug=False)