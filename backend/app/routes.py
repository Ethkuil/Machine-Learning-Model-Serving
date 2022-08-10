from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import os
import random

app = Flask(__name__)
CORS(app, support_credentials=True)
# Get port number from the environment varriable
port = os.getenv("PORT")
# os.path.abspath(os.path.join(os.path.dirname("__file__"),"../.."))

@app.route('/')

@app.route('/index')
def index():
    return 'hello world'

@app.route('/getModelDetail', methods=['GET', 'POST'])
def getModelDetail():
    postData = request.get_json()
    filePathStr = postData.get('filePath')
    from readFile import readFile
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

if __name__ == '__main__':
    print(os.path)
    # If the app is running locally
    if port is None:
    # Use port 5000
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
    # Else use cloud foundry default port
        app.run(host='0.0.0.0', port=int(port), debug=False)