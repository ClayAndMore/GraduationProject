#这个脚本是创建帖子的脚本，在运行python manage.py shell 时 ：
#>>> import fate_data_note.py即可运行

import datetime
from uuid import uuid4
from webapp.models import db,User,Note,Reply,OperationClass

user1=db.session.query(User).filter(User.id==1).first()
user2=db.session.query(User).filter(User.id==2).first()
operationclass1=db.session.query(OperationClass).filter(OperationClass.class2=='普外科').first()

str1='我这个月不小心出了意外，我的右手臂意外骨折。经过医院的处理，我现在在家调养，我想要自己恢复的快点，大家有没有感同身受的建议？'
str2='去年我和你的经历一样，注意尽量休息，多吃些含钙高的东西。'
str3='谢谢你的建议！'

#生成30篇外科帖子：
for i in range(1,30):
    note=Note(id=i,title='外科标题'+str(i),text=str1)
    note.time=datetime.datetime.now()
    note.user_id=user1.id
    note.class_id=operationclass1.id

    reply1=Reply(text=str2)
    reply1.user_id=user2.id
    reply1.note_id=note.id

    reply2=Reply(text=str3)
    reply2.user_id=user1.id
    reply2.note_id=note.id

    db.session.add(note)
    db.session.add(reply1)
    db.session.add(reply2)

db.session.commit()