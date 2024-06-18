# Using flask to make an api 
# import necessary libraries and functions 
from flask import Flask         
from flask_cors import CORS

# Creating an app 
# CORS for deployment connectivity(allow all links)
app = Flask(__name__)
CORS(app)



# on the terminal type: curl http://127.0.0.1:5000/
# returns the data that we send when we use POST.
@app.route('/') 
def index(): 
    """To check whether server is live"""      
    return "The server is running"
  
# importing all controllers from controller folder
from controller import *



