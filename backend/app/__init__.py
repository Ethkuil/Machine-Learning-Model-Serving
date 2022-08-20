from flask import Flask
from flask_cors import CORS

app = Flask(__name__,
            template_folder="../../frontend/dist",
            static_folder="../../frontend/dist/static")  # 需要时可将系统改造为后端渲染

CORS(app, support_credentials=True)

app.config['JSON_AS_ASCII'] = False # 允许中文输出

from app import data

data.dataInit()
