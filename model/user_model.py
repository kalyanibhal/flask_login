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

                # Check for duplicate email
                self.cursor.execute("CREATE TABLE IF NOT EXISTS users(email text primary key, password text)")
                self.cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                
                # Storing first row in count
                count = self.cursor.fetchone()[0]
                
                # Checking for email in the database
                if count > 0:
                    return jsonify({"Prompt": "Email already taken"}), 409

                # PSQL query to add user to database
                self.cursor.execute("INSERT INTO users (email, password) Values(%s, %s)",(email, password)) 
                return jsonify({"Prompt": "User Created Succesfully"}) , 201

    # Checking for existing user
    def user_login_model(self, email):
    
        with self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as self.cursor:

                # Check if email exists
                self.cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))

                # Storing first row in count
                count = self.cursor.fetchone()[0]
                
                # Checking user credentials
                if count > 0:
                    return jsonify({"Prompt":"Login Successful"}), 200
                else:        
                    return jsonify({"Prompt":"You have entered wrong credentials or user doesn't exists"}), 401

            
                