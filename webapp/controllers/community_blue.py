# 这个社区登陆的蓝图

import os
import time

from flask import Blueprint,redirect,url_for,render_template,abort,flash,session,request
from functools import wraps
from datetime import datetime
from webapp.forms import LogInForm,RegisterForm,ChangeImage
from webapp.models import Permission,db,User,Note,OperationClass

from flask_security import login_required,current_user
from flask_security.utils import login_user
from flask_mail import Message
from webapp.extensions import mail,icon
from webapp.fortoken import generote_confirmation_token,back_confirmation_token
from werkzeug.utils import secure_filename
from PIL import Image


# from webapp import app
community_blue = Blueprint(
    'communityBlueName',
    __name__,
    # template_folder=path.join(path.pardir,'templates','main'),
    template_folder='../templates/communityTemp/',
    static_folder='webapp/static/img/avatar'
)

@community_blue.route('/')
def index():
    return redirect('indexBlueName.index')

@community_blue.route('/communityMain.html')
def communityMain():
    username=None
    if current_user.is_authenticated:
        username = current_user._get_current_object().username
    return render_template('communityMain.html',username=username)

@community_blue.route('/communityWaike.html')
@community_blue.route('/communityWaike.html/<int:page>')
def communityWaike(page=1):
    username=None
    if current_user.is_authenticated:
        username = current_user._get_current_object().username

    #定义一个返回的list,包含了所有外科要显示的帖子
    notes=[]
    #查询外科的id,会有很多外科的分类
    wai_ids=db.session.query(OperationClass).filter(OperationClass.class1=='外科').all()
    l=[]
    for x in wai_ids:
        l.append(x.id)

        #根据id查询相关外科的所有帖子,没有返回[]，根据时间来排序,从页数开始，每页返回10个数据
    # wai_notes=db.session.query(Note).filter(Note.class_id.in_(l)).order_by(Note.time).all()
    wai_notes=Note.query.filter(Note.class_id.in_(l)).order_by(Note.time).paginate(page,10,False)

    for temp in wai_notes.items:
        #获得发帖人的相关信息
        publisher=temp.user
        #获得本贴回复的相关信息
        replies_list=[]
        replies=temp.replies.all()

        for reply in replies:
            #组织回帖内容
            reply_data={'user':reply.user.username,
                        'avatar':reply.user.path,
                        'time':reply.confirmed_at,
                        'text':reply.text
            }
            replies_list.append(reply_data)

        #组织回传数据
        data={'id1':'heading'+str(temp.id),  #用于生成标签id
              'id2':'collapse'+str(temp.id),
              'title':temp.title,
              'class':temp.operation_class.class2,
              'time':temp.time,
              'text':temp.text,
              'author':publisher.username,
              'avatar':publisher.path,
              'reply':replies_list}
        notes.append(data)

    for page in wai_notes.iter_pages():
            print(page)
    return render_template('communityWaike.html',
                           username=username,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityWaike")

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

# @community_blue.route('/admin')
# @login_required
# def admin():
#     return render_template('admin/index.html')


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
                login_user(user)
                username=current_user._get_current_object().username
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
                           )

@community_blue.route('/confirm/<token>')
def confirm_token(token):
    from webapp import app
    backEmail=back_confirmation_token(app,token)
    if(backEmail==emailToConfirm):
        user=db.session.query(User).filter(User.email==backEmail).update({User.active:1}).first()

        return '欢迎登陆'


@community_blue.route('/personalInfo.html',methods=['GET','POST'])
@login_required
def persionalInfo():

    form=ChangeImage()
    username = current_user._get_current_object().username
    src = current_user._get_current_object().path

    #换名字
    if request.method=='POST':
        print(1111)
        print(request.values)

    if form.validate_on_submit():
        #获取文件名
        index=src.rfind('/')
        old_filename = src[index+1:]

        # 先删除原有文件
        #当我们不知道当前路径真正的位置我们可以打印
        # print(os.getcwd())
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
        src=r'../../static/img/avatar/'+filename
        current_user._get_current_object().path=src
        db.session.query(User).filter(User.email==email).update({User.path:src})
        db.session.commit()
        return render_template('personalInfo.html', form=form, username=username, src=src)

    return render_template('personalInfo.html',form=form,username=username,src=src)

