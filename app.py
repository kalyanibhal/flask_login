# Import necessary libraries and functions 
from flask import Flask, json
from flask_cors import CORS

# Creating a Flask app 
app = Flask(__name__) 


"""What is Cross-Origin Resource Sharing? Cross-origin 
resource sharing (CORS) is a mechanism for integrating applications. 
CORS defines a way for client web applications that are loaded 
in one domain to interact with resources in a different domain."""
CORS(app)


# Importing all controllers from controller folder
from controller import *


#verfication> database table ek coloum dalenge gmailverfication
#  user click  > user display verification successful (frontend )
#> database update hoga status done u
#user login again 
#verified done> acess granted else go to gmail and verify again













"""token=s.dumps(gmail,salt='email-confirmation-key')
    
    msg=Message('Important Mail',sender='daniyasiddiqui2319@gmail.com',recipients=['danishgreets@gmail.com'])
    link=url_for('confirm',token=token,_external=True)
    msg.body="your confirmation link"+ link
    mail.send(msg)
    return "mail"
    return """



