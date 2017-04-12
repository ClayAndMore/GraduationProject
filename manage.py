import os

from flask_script import Manager,Server
# from flask_migrate import Migrate,MigrateCommand

#这里的webapp实际上是webapp这个文件包的init.py文件
from webapp import create_app
# from webapp import app
from webapp.models import db

from werkzeug.utils import secure_filename

a=secure_filename('../../static/img/avatar/aaa.txt')

str='../../static/img/avatar/aaa.txt'
index=str.rfind('/')
newstr=str[index+1:]

# default to dev config
# zheli环境变量中要输入WEBAPP_ENV的值，set WEBAPP_ENV=dev,shell中python manage.py server

# env = os.environ.get('WEBAPP_ENV', 'dev')
#capitalize()将字符串的第一个字母变成大写,其他字母变小写
# app = create_app('webapp.config.%sConfig' % env.capitalize())
app = create_app('webapp.config.DevConfig')

# migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command("server", Server())
# manager.add_command("show-urls", ShowUrls())
# manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        newstr=newstr
    )

if __name__ == "__main__":
    manager.run()

