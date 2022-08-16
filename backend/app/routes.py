
from flask import Flask, request, jsonify, render_template
from app import app
import datetime
from app import data
from flask_cors import CORS
import os
from .readFile import readFile

# app = Flask(__name__)
# CORS(app, support_credentials=True)
# Get port number from the environment varriable
port = os.getenv("PORT")
# os.path.abspath(os.path.join(os.path.dirname("__file__"),"../.."))

data.dataInit()

@app.route('/')

@app.route('/index')
def index():
    return 'hello world'

@app.route('/getModelDetail', methods=['GET', 'POST'])  #这部分不适用
def getModelDetail():
    postData = request.get_json() #获得上传数据
    filePathStr = postData.get('filePath') #获得文件路径
    x, y = readFile(filePathStr)
    response = {
        'filePath': filePathStr,
        'xNames': [xx.name for xx in x],
        'xDataTypes': [xx.dataType for xx in x],
        'xOpTypes': [xx.opType for xx in x],
        'xValues': [xx.value for xx in x],
        'yNames': [yy.name for yy in y],
        'yDataTypes': [yy.dataType for yy in y],
        'yOpTypes': [yy.opType for yy in y],
        'yValues': [yy.value for yy in y],

    }
    #print('uflux: ', user_list[user])
    return jsonify(response)

@app.route('/models',methods=['POST','GET'])
def models():
    if request.method=='POST':
        modelArgs=request.values.to_dict()
        file=request.files.get('file')
        if file is None:
            return "no file"
            
        
        file_name=file.filename.replace(" ","")
        file_path=os.path.dirname(__file__)+'/upload/'+file_name
        file.save(file_path)
        
        input,target=readFile(file_path)
        inputVariables=[]
        targetVariables=[]
        for ii in input:
            inputVars={}
            inputVars["field"]=ii.name
            inputVars["data_type"]=ii.dataType
            inputVars["op_type"]=ii.opType
            #维度
            inputVariables.append(inputVars)
            pass
        
        for ii in target:
            targetVars={}
            targetVars["field"]=ii.name
            targetVars["data_type"]=ii.dataType
            targetVars["op_type"]=ii.opType
            targetVariables.append(targetVars)
            
            
        
        mymodel=data.myModel(data.dataIndex,modelArgs['name'],modelArgs['description'],modelArgs['type'],file_path,datetime.datetime.now())
        data.dataIndex+=1
        data.addModel(mymodel)
        return_response = {
            "data":{
                "id":mymodel.id,
                "name":mymodel.name,
                "type":mymodel.type,
                "update_time":mymodel.updateTime,
                "description":mymodel.description,
                "input_variables":inputVariables,
                "target_variables":targetVariables,
                #service
            }
        }
        
        return jsonify(return_response)
        
    elif request.method=='GET':
        responseData=[]
        for i in data.modelList:
            responseData.append({
                "id":i.id,
                "name":i.name,
                "type":i.type,
                "update_time":i.updateTime
            })
        return_response={
            "data":responseData
        }    
        return jsonify(return_response)
        
        
        
