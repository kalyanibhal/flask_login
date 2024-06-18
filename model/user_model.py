"""A model file contains an application's data
logic and the core information that the user can access
and manipulate:"""
import sqlite3
from flask import jsonify
# import re  # Import the regular expression module


class user_model():
    # this method is called from user_controller file
    
    def user_addone_model(self,data):    
        username = data['username']
        password = data['password']

        # Username validation
        if len(username) < 3:
            return jsonify({"Prompt":"Username must be at least 3 characters long"})
        
        if not username.isalnum():
            return jsonify({"Prompt":"Username can only contain alphabets and numbers characters"})

        # Password validation
        if len(password) < 8:
            return jsonify({"Prompt":"Password must be at least 8 characters long"})
        # if not re.search(r'\d', password):
            # return "Password must contain at least one number"

        # Generate a tuple containing username and password
        user_data = (username, password)
        
        # Connect to the SQLite database
        con = sqlite3.connect('users_cred.db')
        cur = con.cursor()

        # Check for duplicate username
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ?", (data['username'],))
        count = cur.fetchone()[0]

        if count > 0:
            con.close()
            return jsonify({"Prompt": "Username already taken"})

        # If validation is successful, add user credential to database
        cur.execute("INSERT INTO users (username, password) VALUES(?, ?)", user_data)
        con.commit()
        con.close()
        return jsonify({"Prompt": "User Created Succesfully"})
    
        
    def user_login_model(self, data):
        
        # Generate a tuple containing username and password
        user_data = (data["username"], data["password"])
        
        # Connect to the SQLite database
        con = sqlite3.connect('users_cred.db')
        cur = con.cursor()
        

        # Check if username and password combination exists
        cur.execute("SELECT COUNT(*) FROM users WHERE username = ? AND password = ?", (user_data))
        count = cur.fetchone()[0]
        con.close()

        if count > 0:
            return jsonify({"Prompt":"Login Successful"})
        else:        
            return jsonify({"Prompt": "You have entered wrong credentials"})


