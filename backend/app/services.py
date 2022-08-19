from urllib import response
from app import app, data
from flask import request, jsonify


@app.route('/services', methods=['POST', 'GET'])
def services():
    if request.method == 'GET':
        pass  # TODO
    elif request.method == 'POST':
        pass  # TODO


@app.route('/services/<int:id>', methods=['GET', 'DELETE'])
def service(id):
    if request.method == 'GET':
        pass  # TODO
    elif request.method == 'DELETE':
        pass  # TODO


@app.route('/services/<int:id>/start', methods=['POST'])
def service_start(id):
    pass  # TODO


@app.route('/services/<int:id>/pause', methods=['POST'])
def service_pause(id):
    pass  # TODO


@app.route('/services/<int:id>/predict', methods=['POST'])
def service_predict(id):
    pass  # TODO
