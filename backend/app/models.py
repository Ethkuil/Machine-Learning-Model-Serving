from flask import request, jsonify
from werkzeug.utils import secure_filename
from app import app, data
import datetime
import os
from .utils.readModel import readModel
from .utils.utils import fileExtension


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
