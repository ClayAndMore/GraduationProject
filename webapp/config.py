class Config(object):
    SECRET_KEY='thisisakey' # wtform的加密密钥
    RECAPTCHA_PUBLIC_KEY = "6LeWqhAUAAAAAHCc18ERrNPCAJ8zbPElvmRkciaE"
    RECAPTCHA_PRIVATE_KEY = "6LeWqhAUAAAAAIGbYs3fAYOTJJDSknhbA6LEc-b_"

    MAIL_SERVER = 'smtp.qq.com'  # 电子邮件服务器的主机名或IP地址
    MAIL_PORT = '465'  # 电子邮件服务器的端口
    MAIL_USE_SSL = True  # 启用安全套接层
    MAIL_USERNAME = '422516721@qq.com'  # 邮件账户用户名
    MAIL_PASSWORD = 'mnwasfnnmrnwbgdd'  # 邮件账户的密码

    #图片上传
    from flask_uploads import IMAGES
    UPLOADED_TEST_DEST = r'D:\Pictures\test'
    UPLOADED_TEST_ALLOW = IMAGES #只允许这个格式的上传。

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/graduationdb?charset=utf8'


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/graduationdb?charset=utf8'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # 定义西药跳转到登陆页面时触发的模板
    SECURITY_LOGIN_USER_TEMPLATE='communityTemp/login.html'
    SECURITY_PASSWORD_SALT='activate-salt'