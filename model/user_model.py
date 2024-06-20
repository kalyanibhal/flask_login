import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv
from flask import jsonify

class user_model:
    # Constructor
    def __init__(self):
        # Loads environment variables
        load_dotenv()

        # Establishing Connection   
        url = os.getenv("POSTGRES_URL")
        if not url:
            raise ValueError("POSTGRES_URL environment variable is not set")
        
        try:
            self.connection = psycopg2.connect(url)
        except Exception as e:
            raise ConnectionError(f"Connection Establishment Failed: {e}")

    # For registering a new user
    def user_addone_model(self, email, password):
        if not hasattr(self, 'connection'):
            raise ConnectionError("Database connection is not established")

        # For establishing the connection
        with self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                # Check for duplicate email
                cursor.execute("CREATE TABLE IF NOT EXISTS users(email text primary key, password text)")
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                
                # Storing first row in count
                count = cursor.fetchone()[0]
                
                # Checking for email in the database
                if count > 0:
                    return jsonify({"Prompt": "Email already taken"})

                # PSQL query to add user to database
                cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password)) 
                return jsonify({"Prompt": "User Created Successfully"}), 201

    def user_login_model(self, email):
        if not hasattr(self, 'connection'):
            raise ConnectionError("Database connection is not established")

        with self.connection:
            with self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                # Check if email exists
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))

                # Storing first row in count
                count = cursor.fetchone()[0]
                
                # Checking user credentials
                if count > 0:
                    return jsonify({"Prompt": "Login Successful"}), 200
                else:        
                    return jsonify({"Prompt": "You have entered wrong credentials or user doesn't exist"})