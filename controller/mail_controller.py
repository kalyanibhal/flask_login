from flask import json, url_for, jsonify, render_template
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from app import app
from model.user_model import user_model

# an object is created
obj = user_model()

# Loading configuration from config.json
with open('config.json','r')as f:
    params=json.load(f)['param']

# Configuring Flask-Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=True
app.config['MAIL_DEBUG'] = True   # always add this
app.config["secret_key"]="secret"
app.config['MAIL_DEFAULT_SENDER'] = params['gmail-user']
app.config['SECURITY_PASSWORD_SALT'] = 'password salt'

# Initialize Flask-Mail after configuration  
mail= Mail(app) 
serializer = URLSafeTimedSerializer(app.config['secret_key'])


def generate_confirmation_token(email):
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT']) # Generates a signed token

def send_confirmation_email(user_email):
    token = generate_confirmation_token(user_email) 
    print(token)
    confirm_url = url_for('confirm_email', token=token, _external=True)
    text_body = f'Please click the link to verify your email: {confirm_url}'
    send_email(user_email, "Please confirm your email", text_body)

def send_email(to, subject, body):
    msg = Message(subject, recipients=[to], body=body, sender=app.config['MAIL_USERNAME'])
    mail.send(msg)

@app.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    try:
        email = serializer.loads(token, salt=app.config['SECURITY_PASSWORD_SALT'], max_age=3600)
        try:
            # Changing verification status in DB
            obj.user_verification_model(email)        
        except:
            return jsonify({"Prompt": "Can't access DB"})
        return render_template("confirmation.html") 
    except SignatureExpired:
        return jsonify({"message": "The confirmation link has expired."}), 400
