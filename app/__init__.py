from flask import Flask

from app.ext import init_ext
from app.settings import init_settings
from app.views import init_blue


def create_app(env):
    app = Flask(__name__)
    # flask实例化对象配置
    init_settings(app,env)

    # 插件初始化
    init_ext(app)

    # 蓝图配置
    init_blue(app)

    return app