from webapp.models import db,User,Role,Permission

from flask_login import current_user

from flask_wtf import CSRFProtect
from flask_security import SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import UploadSet


csrf=CSRFProtect()
mail=Mail()

user_datastore=SQLAlchemyUserDatastore(db,User,Role)

icon=UploadSet('TEST')

admin=Admin(name='康复网后台管理', template_mode='bootstrap3')

class needAdminView(ModelView):
    def is_accessible(self):
        #如果没有登陆
        if current_user.roles:
            return current_user.roles[0].permissions==Permission.ADMINISTER
        return False

admin.add_view(needAdminView(User,db.session,name='用户'))
admin.add_view(needAdminView(Role,db.session,name='权限'))


