# Import necessary libraries and functions 
from flask import Flask 
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