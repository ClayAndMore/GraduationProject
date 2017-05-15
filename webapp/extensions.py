from webapp.models import db,User,Role,Permission,Note,Equip,Medicine,Reply

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
        role_list=current_user.roles
        if role_list:
            #遍历用户所有的权限：
            for role in role_list:
               if role.permissions==Permission.ADMINISTER:
                   return True
            # 没有管理员权限
            return False
        # 如果没有登陆
        return False

admin.add_view(needAdminView(User,db.session,name='用户'))
admin.add_view(needAdminView(Role,db.session,name='权限'))
admin.add_view(needAdminView(Note,db.session,name='帖子'))
admin.add_view(needAdminView(Reply,db.session,name='回帖'))
admin.add_view(needAdminView(Equip,db.session,name='设备管理'))
admin.add_view(needAdminView(Medicine,db.session,name='药物管理'))



