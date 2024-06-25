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
        
    return obj.user_login_model(email, password)


# Controller for deleting a user
@app.route('/user/delete', methods=['DELETE'])
def delete_account():

  # Storing recieved data in variable
    data = request.get_json()
    email = data["email"]
    
    if not email:
         return jsonify({'Prompt': 'Email is required'}), 400
    
    return obj.user_delete_model(email)



