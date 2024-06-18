# Import necessary libraries and functions 
import os
import psycopg2 
from dotenv import load_dotenv
from flask import Flask 
from flask_cors import CORS

CREATE_users_TABLE=(
    "CREATE TABLE IF NOT EXISTS users(username PRIMARY KEY, password TEXT)"
)

load_dotenv()


# Creating a Flask app 
app = Flask(__name__) 
url = os.getenv("POSTGRES_URL")
connection = psycopg2.connect(url)

"""What is Cross-Origin Resource Sharing? Cross-origin 
resource sharing (CORS) is a mechanism for integrating applications. 
CORS defines a way for client web applications that are loaded 
in one domain to interact with resources in a different domain."""
CORS(app)




# Importing all controllers from controller folder
from controller import *


