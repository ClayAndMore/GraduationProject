from  flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField,PasswordField,SubmitField,FileField,SelectField,TextAreaField
from wtforms.validators import DataRequired,Length,Email,EqualTo
from flask_security import LoginForm

showRequiredStr="内容不能为空"
showEmailStr="不是正确的邮箱格式"
showPasswdStr="输入的密码长度为6~18"

class LogInForm(FlaskForm):
    email = StringField(
        '登陆邮箱：',
        validators=[DataRequired(message=showRequiredStr),Email(message=showEmailStr)]
    )
    password = PasswordField(
        '密码：',
        validators=[DataRequired(message=showRequiredStr)]
    )
    # recaptcha = RecaptchaField()


class RegisterForm(FlaskForm):
    userEmail=StringField(
        '注册邮箱：',
        validators=[DataRequired(message=showRequiredStr),Email(message=showEmailStr)]
    )
    userName=StringField(
        '用户名：',
        validators=[DataRequired(message=showRequiredStr),Length(min=4,max=8)]
    )
    password = PasswordField(
        validators=[DataRequired(message=showRequiredStr),Length(min=6,max=18,message=showPasswdStr)]
    )
    passwordAgain = PasswordField(
        '确认密码',
        validators=[DataRequired(message=showRequiredStr),EqualTo('password',message='两次密码输入不一致')]
    )
    # recaptcha = RecaptchaField()

class ChangeImage(FlaskForm):
    browse=FileField(
        '上传',
        validators=[DataRequired()]
    )
    upload=SubmitField(
        '完成',
    )

#定义一个发帖的表单
class PostNote(FlaskForm):
    title=StringField(
        '标题',
        validators=[DataRequired()]
    )
    opera_class=SelectField(
        '所属科目',choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')]
    )
    text_area=TextAreaField(
        '正文',
        validators=[DataRequired()])
    post = SubmitField(
        '发帖',
    )