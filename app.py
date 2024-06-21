# Import necessary libraries and functions 
from flask import Flask, request, jsonify ,json
from flask_mail import Mail, Message
from flask_jwt_extended import JWTManager, create_access_token, decode_token#used for creating and verifying JWT tokens
from flask_cors import CORS
from itsdangerous import URLSafeTimedSerializer 
import datetime

#URLSafeTimedSerializer to generate token

# Creating a Flask app 
app = Flask(__name__) 


# Loading configuration from config.json
with open('config.json','r')as f:
    params=json.load(f)['param']

# Configure Flask-JWT-Extended
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
jwt = JWTManager(app)

# Configuring Flask-Mail
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True 
app.config['MAIL_DEBUG'] = True   # always add this
app.config["secret_key"]="secret"
app.config['MAIL_DEFAULT_SENDER'] = params['gmail-user']

# Initialize Flask-Mail after configuration  
# Flask-Mail is initialized before it won't have the necessary information to function correctly
# leading to potential errors and issues.
mail= Mail(app) 

#s=URLSafeTimedSerializer(app.config["secret_key"])

"""What is Cross-Origin Resource Sharing? Cross-origin 
resource sharing (CORS) is a mechanism for integrating applications. 
CORS defines a way for client web applications that are loaded 
in one domain to interact with resources in a different domain."""
CORS(app)


# Importing all controllers from controller folder
from controller import *

#controller for sending email
@app.route('/sendverifylink',methods=["POST"] )
def sendverifylink():
    #fetch the email id
    data = request.get_json()
    gmail = data["email"]

    if not gmail:
        return jsonify({"error": "Email is required"}), 400
    
    # Create a jwt verification token with an expiration time
    expires = datetime.timedelta(hours=1)
    verification_token = create_access_token(identity=gmail, expires_delta=expires)

    #Generate the Verification URL

    verification_url = f"http://yourdomain.com/verify/{verification_token}"

    # sending mail 
    msg = Message('Email Verification', recipients=[gmail])
    msg.body = f'Please verify your email by clicking on the following link: {verification_url}'
    #Send the Email
    mail.send(msg)

    return jsonify({"message": "Verification email sent"}), 200

@app.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    try:
        # Decode the token to get the email
        decoded_token = decode_token(token) # Decode the JWT token that was passed as a parameter in the URL
        email = decoded_token['sub'] # Extract the email from the decoded token
        return jsonify({"message": f"Email {email} verified successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400














    """token=s.dumps(gmail,salt='email-confirmation-key')
    
    msg=Message('Important Mail',sender='daniyasiddiqui2319@gmail.com',recipients=['danishgreets@gmail.com'])
    link=url_for('confirm',token=token,_external=True)
    msg.body="your confirmation link"+ link
    mail.send(msg)
    return "mail"
    return """



