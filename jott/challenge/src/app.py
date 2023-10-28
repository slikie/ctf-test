from flask import Flask, render_template, jsonify, request, redirect, make_response, url_for
from werkzeug.utils import url_quote
import jwt

app = Flask(__name__)

SECRET_KEY = "jott123!"

@app.route('/')
def index():
    image_path = url_for('static', filename='images/notetaking.jpg')
    return render_template('landing.html', image=image_path)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if username == "john_doe" and password == "password123":
            # Encoding the token
            token = jwt.encode({"sub": username, "role": "user"}, SECRET_KEY, algorithm="HS256")
            response = make_response(redirect('/dashboard'))
            response.set_cookie('jwt', token)
            return response
        
        else:
            return render_template('login.html', error="Invalid credentials!")

    return render_template('login.html', error=None)

@app.route('/dashboard')
def dashboard():
    token = request.cookies.get('jwt')    
    if not token:
        return redirect('/login')

    try:
        # Decoding the token
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = decoded_token.get("sub")
        user_notes = users_notes.get(username, [])
        if decoded_token.get('role') == 'admin':
            # Read the content of 'flag.txt'
            with open('flag.txt', 'r') as file:
                flag_content = file.read()
            return render_template('admin_dashboard.html', flag=flag_content)
        else:
            return render_template('user_dashboard.html', notes=user_notes)
    except jwt.ExpiredSignatureError:
        return redirect('/login')
    except jwt.InvalidTokenError:
        return redirect('/login')

@app.route('/is_logged_in', methods=['GET'])
def is_logged_in():
    token = request.cookies.get('jwt_token')

    if not token:
        return jsonify({"logged_in": False}), 200
    
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"logged_in": True}), 200
    except:
        return jsonify({"logged_in": False}), 200


@app.route('/logout', methods=['GET'])
def logout():
    # Check if user has a valid JWT
    token = request.cookies.get('jwt')
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        response = make_response(redirect('/'))
        response.set_cookie('jwt', '', expires=0)  # Clear the JWT
        return response
    except:
        return redirect('/login')  # If no JWT or it's invalid, redirect to login


if __name__ == '__main__':
    app.run(debug=True)
