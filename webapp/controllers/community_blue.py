# 这个社区登陆的蓝图

from flask import Blueprint,redirect,url_for,render_template,abort,flash,session,request
from functools import wraps

from webapp.forms import PostNote
from webapp.models import Permission,db,User,Note,OperationClass

from flask_security import login_required,current_user


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
    return redirect('indexBlueName.index')

@community_blue.route('/communityMain')
def communityMain():
    username,src=isCurrentUser()
    return render_template('communityMain.html',username=username,src=src)

#定义一个方法，加载各科目帖子的方法，达到共用的目的
def getNotes(page,opera_class_name):
    # 定义一个返回的list,包含了所有外科要显示的帖子
    notes = []
    # 查询外科的id,会有很多外科的分类
    wai_ids = db.session.query(OperationClass).filter(OperationClass.class1 == opera_class_name).all()
    l = []
    for x in wai_ids:
        l.append(x.id)

        # 根据id查询相关外科的所有帖子,没有返回[]，根据时间来排序,从页数开始，每页返回10个数据
    # wai_notes=db.session.query(Note).filter(Note.class_id.in_(l)).order_by(Note.time).all()
    wai_notes = Note.query.filter(Note.class_id.in_(l)).order_by(Note.time).paginate(page, 10, False)

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

@community_blue.route('/communityWaike')
@community_blue.route('/communityWaike/<int:page>')
def communityWaike(page=1):
    username,src=isCurrentUser()

    opera_class_name='外科'
    notes,wai_notes=getNotes(page,opera_class_name)

    note_form=PostNote()
    #发帖
    if note_form.validate_on_submit():
        #说明已经登陆
        if username:
            pass
        else:
            return redirect(url_for('communityBlueName.login'))

    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityWaike",
                           note_form=note_form)

@community_blue.route('/communityFuchan')
@community_blue.route('/communityFuchan/<int:page>')
def communityFuchan(page=1):
    username,src = isCurrentUser()
    opera_class_name = '妇产科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityFuchan",
                           note_form=note_form)

@community_blue.route('/communityEye')
@community_blue.route('/communityEye/<int:page>')
def communityEye(page=1):
    username,src = isCurrentUser()
    opera_class_name = '眼科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityEye",
                           note_form=note_form)

@community_blue.route('/communityErbihou')
@community_blue.route('/communityErbihou/<int:page>')
def communityErbihou(page=1):
    username,src= isCurrentUser()
    opera_class_name = '耳鼻喉科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityErbihou",
                           note_form=note_form)

@community_blue.route('/communityKouqiang')
@community_blue.route('/communityKouqiang/<int:page>')
def communityKouqiang(page=1):
    username,src = isCurrentUser()
    opera_class_name = '口腔科'
    notes, wai_notes = getNotes(page, opera_class_name)

    note_form = PostNote()
    return render_template('communityOption.html',
                           username=username,
                           src=src,
                           notes=notes,
                           pagination=wai_notes,
                           endpoint="communityBlueName.communityKouqiang",
                           note_form=note_form)


@community_blue.route('/communityDoctor')
@login_required
def communityDoctor():
    return render_template('communityDoctor.html')

#联系我们
@community_blue.route('/Contact')
def contact():
    return None


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




