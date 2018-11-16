from flask_migrate import MigrateCommand
from flask_script import Manager

from app import create_app

app = create_app("default")
manager = Manager(app)

# 这句话使得模型迁移的命令生效
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()
