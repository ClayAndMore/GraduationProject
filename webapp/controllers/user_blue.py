import datetime,os,time

from flask import Blueprint,redirect,session,render_template,flash,url_for,request

from webapp.models import db,User,Role,Permission
from webapp.forms import LogInForm,RegisterForm,ChangeImage
from webapp.fortoken import generote_confirmation_token,back_confirmation_token
from webapp.extensions import mail,icon

from flask_security import login_user,current_user,login_required,logout_user
from flask_mail import Message
from werkzeug.utils import secure_filename

user_blue = Blueprint(
    'userBlue',
    __name__,
    # template_folder=path.join(path.pardir,'templates','main'),
    template_folder='../templates/communityTemp/user_temp/',
    static_folder='webapp/static/img/avatar'
)

@user_blue.route('/')
def index():
    return redirect('indexBlueName.index')

@user_blue.route('/login.html',methods=['GET','POST'])
def login():
    form=LogInForm()
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
                return render_template('login.html',formHtml=form)

            if user.password==password:
                login_user(user)
                return redirect(url_for('communityBlueName.communityMain'))
            else:
                form.password.errors.append("密码输入错误")
                form.password.data=''
                return render_template('login.html',formHtml=form)
        except Exception as e:
            print(e)
            flash(message="数据库连接异常，请联系管理员")
            # form.email.errors.append("该用户没有注册")
            return redirect(url_for('communityBlueName.login'))
    return render_template('login.html',formHtml=form)

def sendEmail(userEmail):
    # 发送邮件
    from webapp import app
    global emailToConfirm
    emailToConfirm = userEmail
    token = generote_confirmation_token(app, userEmail)
    print(token)
    msg = Message('注册确认', sender=app.config['MAIL_USERNAME'], recipients=[userEmail])
    msg.body = '这是body'
    msg.html = '<b>欢迎注册康复网，请点击下面链接完成用户注册</b>' + app.config['MAIL_TO_BACK']+ 'confirm/' + token
    mail.send(msg)

emailToConfirm=None #用于确认登陆
@user_blue.route('/register.html',methods=['GET','POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        print('注册验证')
        userEmail=form.userEmail.data
        userName=form.userName.data
        password=form.password.data
        user=User(email=userEmail,
                  username=userName,
                  password=password,
                  confirmed_at=datetime.datetime.now())
        #为此用户添加默认权限
        role=db.session.query(Role).filter(Role.permissions==Permission.LOGIN).first()
        user.roles=[role]
        try:
            #邮件字段设置了unique=True，若邮箱重复，则异常
            db.session.add(user)
            db.session.commit()

        except Exception as e1:
            # t, v, tb = sys.exc_info()
            # print(t)
            print('注册异常e1:'+str(e1))
            # 数据回滚
            db.session.rollback()
            # 如果没有激活
            try:
                if not db.session.query(User).filter(User.email==userEmail).first().active:
                    sendEmail(userEmail)    #再次发送邮件
                    return "已发送邮件，请到注册邮箱确认注册"
                else:
                    return '此邮箱已经被注册'
                # flash("此邮箱已经被注册")
            except Exception as e2:
                print('注册异常e2:'+str(e2))
                return "数据库连接异常，请联系管理员"

        sendEmail(userEmail)
        return "已发送邮件，请到注册邮箱确认注册"
    return render_template('register.html',
                           formHtml=form
                           )

@user_blue.route('/confirm/<token>')
def confirm_token(token):
    from webapp import app
    backEmail=back_confirmation_token(app,token)
    if(backEmail==emailToConfirm):
        #将active置1,完成激活。
        #下面这句话返回的是 1，更改过后的数值，而不是user类型。
        # db.session.query(User).filter(User.email==backEmail).update({User.active:1})
        print('111')
        user=db.session.query(User).filter(User.email==backEmail).first()
        print('222')
        user.active=1
        db.session.commit()
        print(user.active)
        login_user(user)
        return redirect(url_for('communityBlueName.communityMain'))
    else:
        print('333')
        return "您的注册信息有风险，请重新注册"

# 定义一个方法，判断是不是当前用户，如果是返回用户名和头像，匿名则返回none
def isCurrentUser():
    if current_user.is_authenticated:
        return current_user._get_current_object().username, current_user._get_current_object().path
    return None, None

#个人信息
@user_blue.route('/personalInfo',methods=['GET','POST'])
@login_required
def persionalInfo():

    form=ChangeImage()
    username,src = isCurrentUser()
    print(src)

    if form.validate_on_submit():
        #获取文件名
        index=src.rfind('/')
        old_filename = src[index+1:]

        #当我们不知道当前路径真正的位置我们可以打印
        # print(os.getcwd())
        #如果不是初次上传头像先删掉又来头像,find 找不到返回-1，并不是0
        print(src.find('avatar'))
        if not src.find('avatar'):
            os.remove(r'static/img/avatar/'+old_filename)

        email = current_user._get_current_object().email
        file=form.browse.data
        #头像缩放
        # im = Image.open(file)
        # size = (60, 60)
        # im.thumbnail(size)
        #头像名字
        filenameTemp=secure_filename(file.filename)
        #.从右侧出现的第一次位置，没有返回-1。这样做是为了获取头像格式
        index=filenameTemp.rfind('.')
        imgStyle=filenameTemp[index:]
        #去掉邮箱名的.,并加上时间戳,并变成秒，保证头像名字的唯一性
        filename=email.replace('.','')+str(int(time.time()*1000))+imgStyle


        icon.save(file, name=filename)
        # im.save(os.path.join(community_blue.static_folder, filename))
        # 这是为模板文件提供的路径
        src=r'../../../static/img/avatar/'+filename
        current_user._get_current_object().path=src
        db.session.query(User).filter(User.email==email).update({User.path:src})
        db.session.commit()
        return render_template('personalInfo.html', form=form, username=username, src=src)

    return render_template('personalInfo.html',form=form,username=username,src=src)

#登出
@user_blue.route('/communityLogout')
def logout():
    logout_user()
    return redirect(url_for('communityBlueName.communityMain'))
