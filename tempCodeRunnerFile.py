
        # You can perform additional verification logic here if needed
        
        return "<h1>Email Verification Successful!</h1>"
    
    except Exception as e:
        print(f"Error: {e}")  # Debug statement to print the error
        return "<h1>Email Verification Failed!</h1>"
    
"""@app.route('/verify/<token>', methods=['GET'])