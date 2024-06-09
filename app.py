# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask, jsonify, request
from flask_cors import CORS


# creating a Flask app 
app = Flask(__name__) 
CORS(app)


# on the terminal type: curl http://127.0.0.1:5000/
# returns hello world when we use GET.
# returns the data that we send when we use POST.
@app.route('/') 
def index(): 
    """To check whether server is live"""
    return "The server is running"
  
# importing all controllers from controller folder
from controller import *


