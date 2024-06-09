"""A model file contains an application's data
logic and the core information that the user can access
and manipulate:"""
import sqlite3

# Connect to the SQLite database

class user_model():
    # this method is called from user_controller file
    def user_addone_model(self,data):    
        user_data = (data['username'], data['password'])
        conn = sqlite3.connect('users_cred.db')
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, password) VALUES(?, ?)",user_data)
        conn.commit()
        conn.close()
        return "User Created Succesfully"
        