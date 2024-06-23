"""
A controller file is responsible for 
controlling how a user interacts with an application.
It contains the flow control logic for an application
and determines what response to send to a user when they make
a browser request.

Data Validation should be carried out here
"""

import re
from flask import request, jsonify
from app import app
# here model.user_model points to the file
# user_model then references the class
from model.user_model import user_model

# an object is created
obj = user_model()


# Default route
@app.route('/') 
def index(): 
    """To check whether server is live"""
    return "The server is running"


# Controller for signing up a user
@app.route('/user/addone', methods = ['POST'])
def user_addone_controller():

    # Storing recieved data in variable
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    
    # Ensure email was submitted
    if not email:
        return jsonify({"Prompt":"must provide email"})

    # Ensure password was submitted
    elif not password:
        return jsonify({"Prompt":"must provide password"})

    # Email validation
    if len(email) < 3:
        return jsonify({"Prompt":"email must be at least 3 characters long"})

    if " " in email:
        return jsonify({"Prompt":"whitespace not allowed"})
        
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):  
        return jsonify({"Prompt":"Please enter a valid E-mail"})  

    # Password Validation
    if " " in password:
        return jsonify({"Prompt":"whitespace not allowed"})

    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        
    if not re.match(pattern, password):
        return jsonify({"Prompt":"The password should contain at least one lowercase letter,\
                         one uppercase letter, one digit, and one special character"})

    return obj.user_addone_model(email, password)


# Controller for logging in
@app.route('/user/login', methods = ['GET'])
def user_login_controller():

    # Storing recieved data in variable
    data = request.get_json()
    email = data["email"]
    password = data["password"]

    # Ensure email was submitted
    if not email:
        return jsonify({"Prompt":"must provide email"})

    # Ensure password was submitted
    elif not password:
        return jsonify({"Prompt":"must provide password"})
        
    return obj.user_login_model(email)


# #controller for sending email
# @app.route('/sendverifylink',methods=["POST"] )
# def sendverifylink():
#     #fetch the email id
#     data = request.get_json()
#     gmail = data["email"]

#     if not gmail:
#         return jsonify({"error": "Email is required"}), 400
    
#     # Create a jwt verification token with an expiration time
#     expires = datetime.timedelta(hours=1)
#     verification_token = create_access_token(identity=gmail, expires_delta=expires)

#     #Generate the Verification URL

#     verification_url = f"http://127.0.0.1:5000/verify/{verification_token}"

#     # sending mail 
#     msg = Message('Email Verification', recipients=[gmail])
#     msg.body = f'Please verify your email by clicking on the following link: {verification_url}'
#     #Send the Email
#     mail.send(msg)

#     return jsonify({"message": "Verification email sent"}), 200

# @app.route('/verify/<token>', methods=['GET'])

# def verify_email(token):
#     try:
#         # Decode the token to get the email
#         decoded_token = decode_token(token) # Decode the JWT token that was passed as a parameter in the URL
#         email = decoded_token['sub'] # Extract the email from the decoded token


#         # Update the database to mark email as verified
#         user = User.query.filter_by(email=email).first()
#         if user:
#             user.verified = True
#             db.session.commit()
#             return jsonify({"message": f"Email {email} verified successfully!"}), 200
#         else:
#             return jsonify({"error": "User not found"}), 404

#     except Exception as e:
#         return jsonify({"error": str(e)}), 400
