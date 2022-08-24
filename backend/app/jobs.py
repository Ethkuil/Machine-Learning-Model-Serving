from flask import request, jsonify, send_file
from werkzeug.utils import secure_filename

import os
from threading import Thread

from app import app
from app.data import JOBS
from app.utils.utils import fileExtension, fileNameWithoutExtension
from app.deploy.jobs import deployJob


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
        modelId = eval(request.form.get('model_id'))
        dataset = request.files.get('input')

        fileName = secure_filename(dataset.filename).replace(" ", "")
        datasetFilePath = f'{os.path.dirname(__file__)}/upload/{fileNameWithoutExtension(fileName)}.{JOBS.nextId}.{fileExtension(fileName)}'
        dataset.save(datasetFilePath)

        jobId = JOBS.addJob(name, modelId).id

        # 新开1个线程执行任务
        Thread(target=deployJob, args=(jobId, datasetFilePath)).start()

        return jsonify({"data": {"id": jobId}})


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
            'model_id': job.modelId,
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

        if job.state != '成功':
            return jsonify({"error": "job not finished"}), 404

        path = job.resultFilePath
        fileName = os.path.basename(path)
        fileName = fileNameWithoutExtension(fileNameWithoutExtension(
            fileName)) + '_result.' + fileExtension(fileName)
        rv = send_file(path, as_attachment=True)
        rv.headers['Content-Disposition'] = 'attachment; filename={}'.format(
            fileName)
        return rv
