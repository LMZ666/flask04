def get_uri(database):
    db = database.get("db") or "mysql"
    driver = database.get("driver") or "pymysql"
    user = database.get("user") or "root"
    passwd = database.get("passwd") or "1234"
    host = database.get("host") or "127.0.0.1"
    port = database.get("port") or "3306"
    dbname = database.get("dbname") or "flask04"
    return "{}+{}://{}:{}@{}:{}/{}".format(db,driver,user,passwd,host,port,dbname)

class Baseenv(object):
    DEBUG = False
    TESTING = False
    # Session, Cookies以及一些第三方扩展都会用到SECRET_KEY值
    SECRET_KEY = "!@#FDSF@#$SDF#%##FSDY%$&"
    # 这句话不用记住，反正执行的时候会报这个错，你把单词复制过来就好，赋值为false
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Developenv(Baseenv):
    DEBUG = True
    # TESTING = True
    # qq邮箱
    MAIL_SERVER = 'smtp.qq.com'
    # 使用的是qq的stmp加密服务端口
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # 默认使用这个邮箱发送
    MAIL_DEFAULT_SENDER = "lmzqqyouxiang@qq.com"
    # 我的qq邮箱smtp授权码
    MAIL_PASSWORD = "oslpkdmbkzjabhcc"
    MAIL_USERNAME = "lmzqqyouxiang@qq.com"

    database = {
        "dbname":"flask04"
    }
    SQLALCHEMY_DATABASE_URI = get_uri(database)


config = {
    "develop":Developenv,
    "default":Developenv
}

def init_settings(app,env):
    app.config.from_object(config.get(env))