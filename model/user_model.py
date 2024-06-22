"""
A model file contains an application's data
logic and the core information that the user can access
and manipulate

Data Verification should be carried out here
(database). 
"""

import os # For accessing environment variable
import psycopg2 # Driver to interact with PSQL
import psycopg2.extras # Allows referencing as dictionary
from dotenv import load_dotenv
from flask import jsonify

load_dotenv()

class user_model():

    # For registering a new user
    def user_addone_model(self, email, password):    
        # For establishing the connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Check for duplicate email
                cursor.execute("CREATE TABLE IF NOT EXISTS users(email text primary key, password text)")
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                
                # Storing first row in count
                count = cursor.fetchone()[0]
                
                # Checking for email in the database
                if count > 0:
                    return jsonify({"Prompt": "Email already taken"})

                # PSQL query to add user to database
                cursor.execute("INSERT INTO users (email, password) Values(%s, %s)",(email, password)) 
                return jsonify({"Prompt": "User Created Succesfully"})

    # Checking for existing user
    def user_login_model(self, email):
    
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Check if email exists
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))

                # Storing first row in count
                count = cursor.fetchone()[0]
                
                # Checking user credentials
                if count > 0:
                    return jsonify({"Prompt":"Login Successful"})
                else:        
                    return jsonify({"Prompt":"You have entered wrong credentials or user doesn't exists"})
                

    

            
                


    