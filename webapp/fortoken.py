from itsdangerous import  URLSafeSerializer

def generote_confirmation_token(app,email):
    serializer=URLSafeSerializer(app.config['SECRET_KEY'],salt=app.config['SECURITY_PASSWORD_SALT'])
    return serializer.dumps(email)

def back_confirmation_token(app,token):
    serializer=URLSafeSerializer(app.config['SECRET_KEY'],salt=app.config['SECURITY_PASSWORD_SALT'])
    return serializer.loads(token)  #返回email
