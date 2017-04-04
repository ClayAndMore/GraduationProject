from webapp.models import db,User,Role

from flask_wtf import CsrfProtect
from flask_security import SQLAlchemyUserDatastore
from flask_mail import Mail
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_uploads import UploadSet

csrf=CsrfProtect()
mail=Mail()

user_datastore=SQLAlchemyUserDatastore(db,User,Role)

icon=UploadSet('TEST')

admin=Admin(name='microblog', template_mode='bootstrap3')
admin.add_view(ModelView(User,db.session))
admin.add_view(ModelView(Role,db.session))


