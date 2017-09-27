# -*- coding:utf-8 -*-
# 这个为手术分类的蓝图
from flask import render_template, Blueprint,request,jsonify
from webapp.models import db,OperationClass,OperationType
from xpinyin import Pinyin


index_blue = Blueprint(
    'indexBlueName',
    __name__,
    template_folder='../templates/',
    # url_prefix="/blog"
)

#首页
@index_blue.route('/')
def index():
    # 获得所有科目
    class_operations = OperationClass.query.all()
    operation_pinyin_dict = {}
    p = Pinyin()
    for operation in class_operations:
        class_name = operation.class1
        if class_name in operation_pinyin_dict:
            pass
        else:
            js_str = ''
            for pinyin in p.get_pinyin(class_name).split('-'):
                js_str+=pinyin
            operation_pinyin_dict[class_name]= js_str +'()'
    return render_template('index.html',operation_pinyin_dict=operation_pinyin_dict)

@index_blue.route('/index/<item>')
def index2(item):
    operationclass = db.session.query(OperationClass).filter(OperationClass.spelling == item).first()
    if operationclass:
        operationtypes=db.session.query(OperationType).filter(OperationType.class_id==operationclass.id).all()
        if operationtypes:
            return render_template('/index/index2.html',
                       operationclass=operationclass,
                       operationtypes=operationtypes
                       )
        else:return '手术科目表操作失败'
    return 'url不正确，手术类别表操作失败'

@index_blue.route('/search')
def search():
    print('访问了/search')
    #如果tosearch没有值，则赋赋值''
    searchStr=request.args.get('tosearch','')
    operationtype=db.session.query(OperationType).filter(OperationType.operation_name==searchStr).first()
    print(operationtype)
    if operationtype:
        # return jsonify(resultList=operationtype.all())
        result={'operation_name':operationtype.operation_name,
                'operation_explain':operationtype.operation_explain,
                'operation_after':operationtype.operation_after,
                'operation_west':operationtype.operation_west,
                'operation_china':operationtype.operation_china}
        return jsonify(result)
    errorStr='您的输入有误'
    print(errorStr)
    return jsonify(errorStr)
