"""A controller file is responsible for 
controlling how a user interacts with an application.
It contains the flow control logic for an application
and determines what response to send to a user when they make
a browser request"""


from flask import request
from app import app
# here model.user_model points to the file
# user_model then references the class
from model.user_model import user_model


# an object is created
obj = user_model()

@app.route('/user/addone', methods = ['POST'])
def user_addone_controller():
    # object calls method
    return obj.user_addone_model(request.form)