# -*- coding:utf-8 -*-
# 这个社区登陆的蓝图

import datetime
from flask import Blueprint,redirect,url_for,render_template,abort,flash,session,request
from functools import wraps

from webapp.forms import PostNote
from webapp.models import Permission,db,User,Note,OperationClass

from flask_security import login_required,current_user,roles_accepted


community_blue = Blueprint(
    'communityBlueName',
    __name__,
    # template_folder=path.join(path.pardir,'templates','main'),
    template_folder='../templates/communityTemp/',
    static_folder='webapp/static/img/avatar'
)


#定义一个方法，判断是不是当前用户，如果是返回用户名和头像，匿名则返回none
def isCurrentUser():
    if current_user.is_authenticated:
        return current_user._get_current_object().username,current_user._get_current_object().path
    return None,None

@community_blue.route('/')
def index():
    return redirect(url_for('indexBlueName.index'))

@community_blue.route('/communityMain')
def communityMain():
    permiss_str=None
    username,src=isCurrentUser()
    #判断当前用户的最高权限
    #如果有用户名，说明已登陆，登陆时才判断权限
    if username:
        #得到该用户的所有权限
        user_roles=current_user._get_current_object().roles
        #将各个权限的权限值取出
        top_role=[]
        for role in user_roles:
            top_role.append(role.permissions)

        #最高权限的值
        max_int=max(top_role)
        #找到最高权限的下标
        temp=top_role.index(max_int)
        #返回该权限的说明,可以去看权限的结构
        permiss_str=user_roles[temp].description

    return render_template('communityMain.html',
                           username=username,src=src,
                           permiss_str=permiss_str)

#定义一个方法，加载各科目帖子的方法，达到共用的目的
def getNotes(page,opera_class_name):
    # 定义一个返回的list,包含了所有外科要显示的帖子
    notes = []
    # 查询外科的id,会有很多外科的分类
    wai_ids = db.session.query(OperationClass).filter(OperationClass.class1 == opera_class_name).all()
    if not wai_ids:
        return None,None
    l = []
    for x in wai_ids:
        l.append(x.id)

        # 根据id查询相关外科的所有帖子,没有返回[]，根据时间来逆向排序,从页数开始，每页返回10个数据
    # wai_notes=db.session.query(Note).filter(Note.class_id.in_(l)).order_by(Note.time).all()
    wai_notes = Note.query.filter(Note.class_id.in_(l)).order_by(Note.time.desc()).paginate(page, 10, False)

    for temp in wai_notes.items:
        # 获得发帖人的相关信息
        publisher = temp.user
        # 获得本贴回复的相关信息
        replies_list = []
        replies = temp.replies.all()

        for reply in replies:
            # 组织回帖内容
            reply_data = {'user': reply.user.username,
                          'avatar': reply.user.path,
                          'time': reply.confirmed_at,
                          'text': reply.text
                          }
            replies_list.append(reply_data)

        # 组织回传数据
        data = {'id1': 'heading' + str(temp.id),  # 用于生成标签id
                'id2': 'collapse' + str(temp.id),
                'title': temp.title,
                'class': temp.operation_class.class2,
                'time': temp.time,
                'text': temp.text,
                'author': publisher.username,
                'avatar': publisher.path,
                'reply': replies_list}
        notes.append(data)
    return notes,wai_notes

#定义一个函数查询所有的手术分类,用于渲染发帖的下拉列表
def queryClass():
    class1_list=[]
    classes=db.session.query(OperationClass).group_by(OperationClass.class1).all()
    for x in classes:
        class1_list.append((x.id,x.class1))
    return class1_list

@community_blue.route('/communityWaike',methods=['GET','POST'])
@community_blue.route('/communityWaike/<int:page>',methods=['GET','POST'])
def communityWaike(page=1):
    username,src=isCurrentUser()

    opera_class_name='外科'
    notes,wai_notes=getNotes(page,opera_class_name)

    note_form=PostNote()
    note_form.opera_class.choices=queryClass()

    #发帖
    if note_form.validate_on_submit():
        #说明已经登陆
        if username:
            title=note_form.title.data
            note_class=note_form.opera_class.data  #得到的是OperationClass中的id
            note_text=note_form.text_area.data
            note_time=datetime.datetime.now()

            note=Note(title=title,text=note_text,time=note_time)
            note.user_id=current_user._get_current_object().id
            note.class_id=note_class

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('communityBlueName.communityWaike'))

        else:
            return redirect(url_for('userBlue.login'))

    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityWaike",
                           note_form=note_form)

@community_blue.route('/communityFuchan',methods=['GET','POST'])
@community_blue.route('/communityFuchan/<int:page>',methods=['GET','POST'])
def communityFuchan(page=1):
    username,src = isCurrentUser()
    opera_class_name = '妇产科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    note_form.opera_class.choices = queryClass()

    # 发帖
    if note_form.validate_on_submit():
        # 说明已经登陆
        if username:
            title = note_form.title.data
            note_class = note_form.opera_class.data  # 得到的是OperationClass中的id
            note_text = note_form.text_area.data
            note_time = datetime.datetime.now()

            note = Note(title=title, text=note_text, time=note_time)
            note.user_id = current_user._get_current_object().id
            note.class_id = note_class

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('communityBlueName.communityFuchan'))

        else:
            return redirect(url_for('userBlue.login'))
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityFuchan",
                           note_form=note_form)

@community_blue.route('/communityEye',methods=['GET','POST'])
@community_blue.route('/communityEye/<int:page>',methods=['GET','POST'])
def communityEye(page=1):
    username,src = isCurrentUser()
    opera_class_name = '眼科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    note_form.opera_class.choices = queryClass()

    # 发帖
    if note_form.validate_on_submit():
        # 说明已经登陆
        if username:
            title = note_form.title.data
            note_class = note_form.opera_class.data  # 得到的是OperationClass中的id
            note_text = note_form.text_area.data
            note_time = datetime.datetime.now()

            note = Note(title=title, text=note_text, time=note_time)
            note.user_id = current_user._get_current_object().id
            note.class_id = note_class

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('communityBlueName.communityEye'))

        else:
            return redirect(url_for('userBlue.login'))
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityEye",
                           note_form=note_form)

@community_blue.route('/communityErbihou',methods=['GET','POST'])
@community_blue.route('/communityErbihou/<int:page>',methods=['GET','POST'])
def communityErbihou(page=1):
    username,src= isCurrentUser()
    opera_class_name = '耳鼻喉科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    note_form.opera_class.choices = queryClass()

    # 发帖
    if note_form.validate_on_submit():
        # 说明已经登陆
        if username:
            title = note_form.title.data
            note_class = note_form.opera_class.data  # 得到的是OperationClass中的id
            note_text = note_form.text_area.data
            note_time = datetime.datetime.now()

            note = Note(title=title, text=note_text, time=note_time)
            note.user_id = current_user._get_current_object().id
            note.class_id = note_class

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('communityBlueName.communityErbihou'))

        else:
            return redirect(url_for('userBlue.login'))
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityErbihou",
                           note_form=note_form)

@community_blue.route('/communityKouqiang',methods=['GET','POST'])
@community_blue.route('/communityKouqiang/<int:page>',methods=['GET','POST'])
def communityKouqiang(page=1):
    username,src = isCurrentUser()
    opera_class_name = '口腔科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    note_form.opera_class.choices = queryClass()

    # 发帖
    if note_form.validate_on_submit():
        # 说明已经登陆
        if username:
            title = note_form.title.data
            note_class = note_form.opera_class.data  # 得到的是OperationClass中的id
            note_text = note_form.text_area.data
            note_time = datetime.datetime.now()

            note = Note(title=title, text=note_text, time=note_time)
            note.user_id = current_user._get_current_object().id
            note.class_id = note_class

            db.session.add(note)
            db.session.commit()

            return redirect(url_for('communityBlueName.communityKouqiang'))

        else:
            return redirect(url_for('userBlue.login'))
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityKouqiang",
                           note_form=note_form)


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def _deco(*args,**kwargs):
            if not current_user.can(permission):
                abort(403,'you can\'t browse it because no permission')
            return f(*args,**kwargs)
        return _deco
    return decorator
#定义一个医生权限的装饰器
def doctor_required(f):
    return permission_required(Permission.OPERATOR)(f)
#管理员的权限
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


@community_blue.route('/communityDoctor',)
@login_required
# @roles_accepted('opera', 'admin')
@doctor_required
def communityDoctor():
    username, src = isCurrentUser()
    return render_template('communityDoctor.html',
                           username=username,
                           src=src,
                           )
#返回主页
@community_blue.route('/back')
def back_home():
    return redirect(url_for('indexBlueName.index'))

#联系我们
@community_blue.route('/Contact')
def contact():
    return None






