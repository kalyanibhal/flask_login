from app import app

@app.route('/user')
def userlogin():
    return "this is login operation"