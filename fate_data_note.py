#这个脚本是创建帖子的脚本，在运行python manage.py shell 时 ：
#>>> import fate_data_note.py即可运行

import datetime
from uuid import uuid4
from webapp.models import db,User,Note,Reply,OperationClass,Role,Permission
# user1=db.session.query(User).filter(User.id==1).first()
# user2=db.session.query(User).filter(User.id==2).first()
# user3=db.session.query(User).filter(User.id==3).first()

# 添加权限
# for num,description in Permission.PERMISSION_MAP.items():
#     role=Role(name=description[0],permission=num,description=description[1])
#     db.session.add(role)
# db.session.commit()

# -----------------------------
# 添加的是妇科帖子
# operationclass1=db.session.query(OperationClass).filter(OperationClass.class2=='妇科').first()
# note1=Note(id=30,title='最近小腹疼，怎么办？>_<',text='最近吃冰点发现，每次都是小腹疼，大家有什么见解？')
# note1.time=datetime.datetime.now()
# note1.user_id=user1.id
# note1.class_id=operationclass1.id
# #     note.user_id=user1.id
# str='当然不要总吃凉的了，尽快去医院检查'
#
# db.session.add(note1)
#
# #十五条回复
# for x in range(15):
#     reply= Reply(text=str+x.__str__(),confirmed_at=datetime.datetime.now())
#     reply.user_id=user1.id
#     reply.note_id=note1.id
#     db.session.add(reply)
# db.session.commit()

#--------------------------------添加的是外科帖子
# operationclass1=db.session.query(OperationClass).filter(OperationClass.class2=='普外科').first()
#
# str1='我这个月不小心出了意外，我的右手臂意外骨折。经过医院的处理，我现在在家调养，我想要自己恢复的快点，大家有没有感同身受的建议？'
# str2='去年我和你的经历一样，注意尽量休息，多吃些含钙高的东西。'
# str3='谢谢你的建议！'
#
# #生成30篇外科帖子：
# for i in range(1,30):
#     note=Note(id=i,title='外科标题'+str(i),text=str1)
#     note.time=datetime.datetime.now()
#     note.user_id=user1.id
#     note.class_id=operationclass1.id
#
#     reply1=Reply(text=str2)
#     reply1.user_id=user2.id
#     reply1.note_id=note.id
#
#     reply2=Reply(text=str3)
#     reply2.user_id=user1.id
#     reply2.note_id=note.id
#
#     db.session.add(note)
#     db.session.add(reply1)
#     db.session.add(reply2)
#
# db.session.commit()