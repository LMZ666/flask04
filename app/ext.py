from flask_bootstrap import Bootstrap
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

db = SQLAlchemy()
# 这里需要注意想起来，如果要使用模型迁移命令需要在manage.py文件中添加command
migrate = Migrate()
cache = Cache(config={
    "CACHE_TYPE":"simple"
})

def init_ext(app):
    db.init_app(app)
    migrate.init_app(app,db=db)
    Bootstrap(app=app)
    cache.init_app(app)