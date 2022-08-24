from urllib import response
from app import app
from flask import request, jsonify

from .data import JOBS


@app.route('/jobs', methods=['GET', 'POST'])
def jobs():
    if request.method == 'GET':
        responseData = [{
            'id': job.id,
            'name': job.name,
            'start_time': job.startTime,
            'state': job.state,
        } for job in JOBS.getJobs() if job]
        return jsonify({'data': responseData})

    elif request.method == 'POST':
        name = request.form.get('name')
        modelId = request.form.get('model_id')
        if not name or not modelId:
            return jsonify({'error': 'name or model_id is missing'}), 400
        # TODO: 添加任务
        # 新开1个线程，运行任务。相关代码新建个deploy文件夹放置，是部署时要拖进容器的。

        # 任务成功添加后
        job = JOBS.addJob(name, modelId)
        return jsonify({"data": {"id": job.id}})


@app.route('/jobs/<int:id>', methods=['GET', 'DELETE'])
def job(id):
    if request.method == 'DELETE':
        try:
            return jsonify({"data": "success"}) if JOBS.deleteJob(id) else (
                jsonify({"error": "job not found"}), 404)
        except IndexError:
            return jsonify({"error": "job not found"}), 404

    elif request.method == 'GET':
        try:
            job = JOBS.getJob(id)
            if not job:
                return jsonify({"error": "job not found"}), 404
        except IndexError:
            return jsonify({"error": "job not found"}), 404
        responseData = {
            'id': job.id,
            'name': job.name,
            'start_time': job.startTime,
            'state': job.state,
            'model': job.model,
        }
        return jsonify({'data': responseData})


@app.route('/jobs/<int:id>/download', methods=['GET'])
def download(id):
    if request.method == 'GET':
        try:
            job = JOBS.getJob(id)
            if not job:
                return jsonify({"error": "job not found"}), 404
        except IndexError:
            return jsonify({"error": "job not found"}), 404
        if job.state != 'success':
            return jsonify({"error": "job not finished"}), 404
        # TODO: 添加下载文件的逻辑
        # 返回二进制文件. application/octet-stream
        path = job.resultFilePath