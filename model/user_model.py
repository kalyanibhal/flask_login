"""
A model file contains an application's data
logic and the core information that the user can access
and manipulate

Data Verification should be carried out here
(database). 
"""
import re
import os # For accessing environment variable
import psycopg2 # Driver to interact with PSQL
import psycopg2.extras # Allows referencing as dictionary
from dotenv import load_dotenv
from flask import jsonify 
from werkzeug.security import generate_password_hash, check_password_hash

load_dotenv()

class user_model():

    # For registering a new user
    def user_addone_model(self, email, password):    
        # For establishing the connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                from controller import mail_controller
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
                cursor.execute("INSERT INTO users (email, password) Values(%s, %s)",(email, generate_password_hash(password))) 

                # Send email with confirmation link
                mail_controller.send_confirmation_email(email) 
                return jsonify({"Prompt": "A confirmation email has been sent to registered Email"})

    # Checking for existing user
    def user_login_model(self, email, password):
    
        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                from controller import mail_controller
                # Check if email exists
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

                # Storing count of occurence
                row = cursor.fetchone()

                # Checking user credentials
                if row is None or not check_password_hash(row["password"], password):
                    return jsonify({"Prompt":"You have entered wrong credentials or user doesn't exists"})
                    
                # Checking whether account is verified or not
                is_active = row["is_active"] 
                
                if is_active == True: 
                    return jsonify({"Prompt":"Login Successful"})
                else:
                    # Send email with confirmation link
                    mail_controller.send_confirmation_email(email)
                    return jsonify({"Prompt":"Please verify your account. A new verification link has been sent"})

    # Changing verification status                
    def user_verification_model(self, email):

        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # Update user verification status
                cursor.execute("UPDATE users SET is_active = TRUE WHERE email = %s",(email,))

    # Delete user credentials
    def user_delete_model(self, email):
      
        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:

                # checking email
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

                # Storing count of occurence
                user = cursor.fetchone()
    
                if not user:        
                    return jsonify({'Prompt': 'User not found'}), 404

                # deleteing the user 
                cursor.execute("DELETE FROM users WHERE email = %s", (email,))
                return jsonify({'Prompt': 'User deleted successfully'})    

    # Verifying user credentials for forget password          
    def user_forget_model(self, email):
      
        # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                from controller import mail_controller 

                # checking email
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))

                # Storing row
                user = cursor.fetchone()
    
                if user:  
                     # Send email with confirmation link
                    mail_controller.send_reset_email(email)       
                    return jsonify({'Prompt': 'Reset email sent sucessfully'})

                if not user:        
                    return jsonify({'Prompt': 'User not found please enter a valid email'}), 404           


    # Changing password status                 
    def user_resetpass_model(self, email, password):   

    # Establishing Connection
        url = os.getenv("POSTGRES_URL")
        connection = psycopg2.connect(url)
        with connection:
            with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                
                # Ensure password was submitted
                if not password:
                    return jsonify({"Prompt":"must provide password"})

                # Password Validation
                if " " in password:
                    return jsonify({"Prompt":"whitespace not allowed"})

                pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        
                if not re.match(pattern, password):
                    return jsonify({"Prompt":"The password should contain at least one lowercase letter, one uppercase letter, one digit, and one special character"})

                # Update the user's password in the database
                cursor.execute("UPDATE users SET password = %s WHERE email = %s", (generate_password_hash(password),email))          
                return jsonify({"Prompt": "Password has been updated successfully"}), 200


    