from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin,UserMixin
from functools import reduce  # 看源码
from operator import or_  # 与操作，可进入看源码

db = SQLAlchemy()

#权限定义
class Permission(object):
    LOGIN=0x01
    EDITOR=0x02
    OPERATOR=0x04
    ADMINISTER=0xff
    PERMISSION_MAP={
        LOGIN:('login','Login user'),
        EDITOR:('editor','Editor'),
        OPERATOR:('op','Operator'),
        ADMINISTER:('admin','Super administrator')
    }

#用户和权限的关系表
roles_users=db.Table(
    'roles_users',
    db.Column('user_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('role_id',db.Integer,db.ForeignKey('role.id'))
)

#定义权限的数据模型(角色）
class Role(db.Model,RoleMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),unique=True)
    permissions=db.Column(db.Integer,default=Permission.LOGIN)
    description=db.Column(db.String(255))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    email=db.Column(db.String(255),unique=True)
    username = db.Column(db.String(255))
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())   #定义是否点击邮箱中的确认链接
    image=db.Column(db.LargeBinary())   #储存头像
    confirmed_at=db.Column(db.DateTime())

    roles=db.relationship('Role',secondary=roles_users,backref=db.backref('user',lazy='dynamic'))

    def __init__(self,email,username,password,confirmed_at):
        self.email=email
        self.username=username
        self.password=password
        self.confirmed_at=confirmed_at

    def can(self,permissions):
        if self.roles is None:
            return False
        all_perms=reduce(or_,map(lambda x:x.permissions,self.roles)) #权限相与
        return all_perms & permissions == permissions #和目标权限相比
    def can_admin(self):
        return self.can(Permission.ADMINISTER)

#手术和药物的关系表
operations_medicines=db.Table(
    'operations_medicines',
    db.Column('operation_id',db.Integer,db.ForeignKey('operation_type.id')),
    db.Column('medicine_id',db.Integer,db.ForeignKey('medicine.id'))
)

#手术和设备的关系表
operations_equips=db.Table(
    'operations_equip',
    db.Column('operation_id', db.Integer, db.ForeignKey('operation_type.id')),
    db.Column('equip_id',db.Integer,db.ForeignKey('equip.id'))
)

# 手术类型
class OperationType(db.Model):
    __tablename__ = 'operation_type'
    id=db.Column(db.Integer(),primary_key=True)
    class_id=db.Column(db.Integer())  #存储手术分组的id
    operation_name=db.Column(db.String(30))
    operation_explain=db.Column(db.String(255)) #手术介绍
    operation_after=db.Column(db.String(255)) #术后处理
    operation_west=db.Column(db.String(255)) #西医处理
    operation_china=db.Column(db.String(255)) #中医处理

    # 药物和设备都是多对多的关系
    medicines=db.relationship('Medicine',secondary=operations_medicines,backref=db.backref('operation_type',lazy='dynamic'))
    equips=db.relationship('Equip',secondary=operations_equips,backref=db.backref('operation_type',lazy='dynamic'))

    @property
    def serialize(self):
        return {
            'id':self.id,
            'class_id':self.class_id,
            'operation_name':self.operation_name,
            'operation_explain':self.operation_explain,
            'operation_after':self.operation_after,
            'operation_west':self.operation_west,
            'operation_china':self.operation_china
        }

class Medicine(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    medicine_name=db.Column(db.String(60))
    medicine_other=db.Column(db.String(255))

class Equip(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    equip_name=db.Column(db.String(60))
    equip_other=db.Column(db.String(255))

#定义手术分类
class OperationClass(db.Model):
    __tablename__ = 'operation_class'
    id=db.Column(db.Integer(),primary_key=True)
    class1=db.Column(db.String(30))
    class2=db.Column(db.String(30))
    spelling=db.Column(db.String(30))
    introduce=db.Column(db.String(255))