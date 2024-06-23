"""
A model file contains an application's data
logic and the core information that the user can access
and manipulate

Data Verification should be carried out here
(database). 
"""

from controller import mail_controller
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
        print(url)
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Check for duplicate email
                cursor.execute("CREATE TABLE IF NOT EXISTS users(email TEXT PRIMARY KEY,\
                                password TEXT, is_active BOOLEAN DEFAULT FALSE)")
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                
                # Storing first row in count
                count = cursor.fetchone()[0]
                
                # Checking for email in the database
                if count > 0:
                    return jsonify({"Prompt": "Email already taken"})

                # PSQL query to add user to database
                cursor.execute("INSERT INTO users (email, password) Values(%s, %s)",(email, password)) 

                # Send email with confirmation link
                mail_controller.send_confirmation_email(email) 
                return jsonify({"Prompt": "A confirmation email has been sent to registered Email"})

    # Checking for existing user
    def user_login_model(self, email):
    
        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Check if email exists
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))

                # Storing count of occurence
                count = cursor.fetchone()[0]

                # Checking user credentials
                if count > 0:
                    cursor.execute("SELECT is_active FROM users WHERE email = %s", (email,))
                    is_active = cursor.fetchone()[0]
                    # Checking if account is verified or not
                    if is_active == True: 
                        return jsonify({"Prompt":"Login Successful"})
                    else:
                        # Send email with confirmation link
                        mail_controller.send_confirmation_email(email)
                        return jsonify({"Prompt":"Please verify your account. A new verification link has been sent"})
                else:        
                    return jsonify({"Prompt":"You have entered wrong credentials or user doesn't exists"})

    # Changing verification status                
    def user_verification_model(self, email):

        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Update user verification status
                cursor.execute("UPDATE users SET is_active = TRUE WHERE email = %s",(email,))
        

    

            
                


    