# Import necessary libraries and functions 
from flask import Flask,json 
from flask_mail import *
from flask_cors import CORS

# Creating a Flask app 
app = Flask(__name__) 

with open('config.json','r')as f:
    params=json.load(f)['param']

mail=Mail(app)    


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT']=465
app.config['MAIL_USERNAME']=params['gmail-user']
app.config['MAIL_PASSWORD']=params['gmail-password']
app.config['MAIL_USE_TLS']=False
app.config['MAIL_USE_SSL']=True 



"""What is Cross-Origin Resource Sharing? Cross-origin 
resource sharing (CORS) is a mechanism for integrating applications. 
CORS defines a way for client web applications that are loaded 
in one domain to interact with resources in a different domain."""
CORS(app)


# Importing all controllers from controller folder
from controller import *

@app.route('/send/mail', methods=['GET'])
def send_mail():
    msg=Message('Important Mail',sender='daniyasiddiqui2319@gmail.com',recipients=['danishgreets@gmail.com'])
    msg.body="sending email link"
    mail.send(msg)
    return "mail"
    



