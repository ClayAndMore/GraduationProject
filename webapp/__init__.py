from flask import Flask,redirect,url_for,request,flash
# from webapp.config import DevConfig

from webapp.models import db,User
from webapp.controllers.community_blue import community_blue
from webapp.controllers.index import index_blue
from webapp.controllers.user_blue import user_blue
from webapp.forms import LogInForm

from webapp.extensions import user_datastore,admin,mail,icon,csrf


from flask_security import Security
from flask_uploads import configure_uploads

def create_app(object_name):
    app=Flask(__name__)
    app.config.from_object(object_name)

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    configure_uploads(app, icon)

    admin.init_app(app)

    app.register_blueprint(index_blue)
    app.register_blueprint(community_blue)
    app.register_blueprint(user_blue)

    return app

app=create_app('webapp.config.DevConfig')

# configure_uploads(app,icon)

security = Security(app, user_datastore)#login_form=LogInForm

#社区医生选项卡，权限页面，不支持工厂模式创建，只能在app初始后再定义
@security.login_context_processor
def security_login_context_processor():
    print(11111)
    form = LogInForm(request.form)

    if form.validate_on_submit():
        userEmail = form.email.data
        password = form.password.data
        try:
            user = db.session.query(User).filter(User.email == userEmail).first()
            # 当输入没有注册的邮箱时，会返回user=None
            if not user:
                form.email.errors.append("该用户没有注册")
                form.email.data = ''
                return dict(formHtml=form)

            if user.password == password:
                return True
            else:
                form.password.errors.append("密码输入错误")
                form.password.data = ''
                return dict(formHtml=form)
        except:
            flash(message="数据库连接异常，请联系管理员")
            # form.email.errors.append("该用户没有注册")
            return dict(formHtml=form)
    return dict(formHtml=form)

#在IDE中点击运行会在这里开始走，而在manage.py里运行shell 命令不会从这里走 会从manage里走。
if __name__ == '__main__':

    app.run()
