# -*- coding:utf-8 -*-
import os

from flask_script import Manager,Server
from flask_migrate import Migrate,MigrateCommand

#这里的webapp实际上是webapp这个文件包的init.py文件
from webapp import create_app

from webapp.models import db,User,Role,Permission,Note,Reply,OperationClass

from werkzeug.utils import secure_filename


# default to dev config
# zheli环境变量中要输入WEBAPP_ENV的值，set WEBAPP_ENV=dev,shell中python manage.py server

# env = os.environ.get('WEBAPP_ENV', 'dev')
#capitalize()将字符串的第一个字母变成大写,其他字母变小写
# app = create_app('webapp.config.%sConfig' % env.capitalize())
app = create_app('webapp.config.DevConfig')

migrate = Migrate(app, db)

from flask import session,request,flash
from flask_security import Security,login_user
from webapp.controllers import  user_blue
from webapp.extensions import user_datastore
from webapp.forms import LogInForm

security = Security(app, user_datastore,register_blueprint=user_blue)#login_form=LogInForm

#需要登陆的权限页面，不支持工厂模式创建，只能在app初始后再定义
@security.login_context_processor
def security_login_context_processor():
    form = LogInForm(request.form)
    if form.validate_on_submit():

        userEmail=form.email.data
        password=form.password.data

        # 刷新页面处理，刷新后让原来填的内容不在留在页面
        session['email']=userEmail
        form.email.data=''

        try:
            user=db.session.query(User).filter(User.email==userEmail).first()
            # 当输入没有注册的邮箱时，会返回user=None
            if not user:
                form.email.errors.append("该用户没有注册")
                form.email.data=''
                return dict(formHtml=form)

            if user.password==password:
                login_user(user)
                return True
            else:
                form.password.errors.append("密码输入错误")
                form.password.data=''
                return dict(formHtml=form)
        except Exception as e:
            print(e)
            flash(message="数据库连接异常，请联系管理员")
            # form.email.errors.append("该用户没有注册")
            return dict(formHtml=form)
    return dict(formHtml = form)

manager = Manager(app)

manager.add_command("server", Server(host='0.0.0.0',port=8080))
# manager.add_command("show-urls", ShowUrls())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    return dict(
        app=app,
        db=db,
        User=User,
        Role=Role,
        Permission=Permission,
        Note=Note,
        Reply=Reply,
        OperationClass=OperationClass
    )

if __name__ == "__main__":
    manager.run()

