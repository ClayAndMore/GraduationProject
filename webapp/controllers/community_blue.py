# 这个社区登陆的蓝图

from flask import Blueprint,redirect,url_for,render_template,abort,flash,session,request
from functools import wraps
from datetime import datetime
from webapp.forms import LogInForm,RegisterForm,ChangeImage
from webapp.models import Permission,db,User

from flask_security import login_required,current_user
from flask_mail import Message
from webapp.extensions import mail,icon
from webapp.fortoken import generote_confirmation_token,back_confirmation_token
from werkzeug.utils import secure_filename

username=None#如果没有登陆用户名一直为空

# from webapp import app
community_blue = Blueprint(
    'communityBlueName',
    __name__,
    # template_folder=path.join(path.pardir,'templates','main'),
    template_folder='../templates/communityTemp/'
)

@community_blue.route('/')
def index():
    return redirect('indexBlueName.index')

@community_blue.route('/communityMain.html')
def communityMain():
    return render_template('communityMain.html')

@community_blue.route('/communityWaike.html')
def communityWaike():
    return render_template('communityWaike.html',username=username)

@community_blue.route('/communityDoctor.html')
@login_required
def communityDoctor():
    return render_template('communityDoctor.html')


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def _deco(*args,**kwargs):
            if not current_user.can(permission):
                abort(403,'您没有权限访问')
            return f(*args,**kwargs)
        return _deco
    return decorator

def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

@community_blue.route('/admin')
@login_required
def admin():
    return render_template('admin/index.html')


@community_blue.route('/login.html',methods=['GET','POST'])
def login():
    form=LogInForm()
    if form.validate_on_submit():

        userEmail=form.email.data
        password=form.password.data
        print(userEmail)

        # 刷新页面处理，刷新后让原来填的内容不在留在页面
        session['email']=userEmail
        form.email.data=''

        try:
            user=db.session.query(User).filter(User.email==userEmail).first()
            # 当输入没有注册的邮箱时，会返回user=None
            if not user:
                form.email.errors.append("该用户没有注册")
                form.email.data=''
                return render_template('login.html',formHtml=form)

            if user.password==password:
                global username  #这样定义就使函数外之前定义的那个username 生效
                username=user.username
                return render_template('communityMain.html',formHtml=form,username=username)
            else:
                form.password.errors.append("密码输入错误")
                form.password.data=''
                return render_template('login.html',formHtml=form)
        except:
            flash(message="数据库连接异常，请联系管理员")
            # form.email.errors.append("该用户没有注册")
            return redirect(url_for('communityBlueName.login'))
    return render_template('login.html',formHtml=form)
#

emailToConfirm=None #用于确认登陆
@community_blue.route('/register.html',methods=['GET','POST'])
def register():
    # userEmail=None
    # userName=None
    # password=None
    # passwordAgain=None
    form=RegisterForm()
    if form.validate_on_submit():
        print('注册验证')
        userEmail=form.userEmail.data
        userName=form.userName.data
        password=form.password.data
        user=User(email=userEmail,
                  username=userName,
                  password=password,
                  confirmed_at=datetime.now())
        try:
            #邮件字段设置了unique=True，若邮箱重复，则异常
            db.session.add(user)
            db.session.commit()
        except:
            # flash("此邮箱已经被注册")
            # return redirect("register.html")
            return "此邮箱已经被注册"

        #发送邮件
        from webapp import app
        emailToConfirm=userEmail
        token=generote_confirmation_token(app,userEmail)
        print(token)
        msg = Message('注册确认', sender=app.config['MAIL_USERNAME'], recipients=[userEmail])
        msg.body = '这是body'
        msg.html = '<b>欢迎注册康复网，请点击下面链接完成用户注册</b>'+'http://127.0.0.1:5000/confirm/'+token
        mail.send(msg)

        return "注册成功，请到注册邮箱确认注册"
    return render_template('register.html',
                           formHtml=form
                           # emailHtml=userEmail,
                           # usernameHtml=userName,
                           # passwordHtml=password,
                           # passwordAgainHtml=passwordAgain
                           )

@community_blue.route('/confirm/<token>')
def confirm_token(token):
    from webapp import app
    backEmail=back_confirmation_token(app,token)
    if(backEmail==emailToConfirm):
        user=db.session.query(User).filter(User.email==backEmail).update({User.active:1}).first()

        return '欢迎登陆'


@community_blue.route('/personalInfo.html',methods=['GET','POST'])
def persionalInfo():
    form=ChangeImage()
    if form.validate_on_submit():
        print(111)
        file=form.browse.data
        filename=secure_filename(file.filename)
        icon.save(file,name=filename)
        return '上传完成'
    return render_template('personalInfo.html',form=form)
