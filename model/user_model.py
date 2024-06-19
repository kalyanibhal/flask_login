"""
A model file contains an application's data
logic and the core information that the user can access
and manipulate

Data Verification should be carried out here. 
"""

import os # For accessing environment variable
import psycopg2 # Driver to interact with PSQL
import psycopg2.extras # Allows referencing as dictionary
from dotenv import load_dotenv
from flask import jsonify

class user_model():

    # Constructor
    def __init__(self):

        # Loads environment variables
        load_dotenv()

        # Establishing Connection   
        url = os.getenv("POSTGRES_URL")
        try:
            self.connection = psycopg2.connect(url)
        except:
            print("Connection Establishment Failed")

    # For registering a new user
    def user_addone_model(self, email, password):    
        # For establishing the connection
        with self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as self.cursor:
                # For PSQL query
                self.cursor.execute("create table if not exists users(email text primary key, password text)")
                self.cursor.execute("INSERT INTO users (email, password) Values(%s, %s)",(email, password)) 
                return jsonify({"Prompt": "User Created Succesfully"}) 


#         email = data['email']
#         password = data['password']

        
#         if not email.isalnum():
#             return jsonify({"Prompt":"email can only contain alphabets and numbers characters"})

#         # Password validation
#         if len(password) < 8:
#             return jsonify({"Prompt":"Password must be at least 8 characters long"})
#         # if not re.search(r'\d', password):
#             # return "Password must contain at least one number"

#         # Generate a tuple containing email and password
#         user_data = (email, password)
        
#         # Connect to the SQLite database
#         con = sqlite3.connect('users_cred.db')
#         cur = con.cursor()

#         # Check for duplicate email
#         cur.execute("SELECT COUNT(*) FROM users WHERE email = ?", (data['email'],))
#         count = cur.fetchone()[0]

#         if count > 0:
#             con.close()
#             return jsonify({"Prompt": "email already taken"})

#         # If validation is successful, add user credential to database
#         cur.execute("INSERT INTO users (email, password) VALUES(?, ?)", user_data)
#         con.commit()
#         con.close()
#         return jsonify({"Prompt": "User Created Succesfully"})
    
        
#     def user_login_model(self, data):
        
#         # Generate a tuple containing email and password
#         user_data = (data["email"], data["password"])
        
#         # Connect to the SQLite database
#         con = sqlite3.connect('users_cred.db')
#         cur = con.cursor()
        

#         # Check if email and password combination exists
#         cur.execute("SELECT COUNT(*) FROM users WHERE email = ? AND password = ?", (user_data))
#         count = cur.fetchone()[0]
#         con.close()

#         if count > 0:
#             return jsonify({"Prompt":"Login Successful"})
#         else:        
#             return jsonify({"Prompt": "You have entered wrong credentials"})
