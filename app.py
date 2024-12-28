from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'a4a4a54s54d54f5f4g65hj41u65j13u1j56n16541hy84h65'

# MongoDB setup
app.config["MONGO_URI"] = "mongodb://localhost:27017/auth_db"
mongo = PyMongo(app)

# Signup Route
@app.route('/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        mobile = request.form['mobile']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        # Check if password matches confirm password
        if password != confirm_password:
            flash('Passwords do not match. Please try again.', 'danger')
            return redirect(url_for('signup'))

        # Check if user already exists
        user = mongo.db.users.find_one({'username': username})
        if user:
            flash('Username already exists. Please choose another.', 'danger')
            return redirect(url_for('signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Insert the user into the database
        mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'mobile': mobile,
            'password': hashed_password
        })

        flash('Signup successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Find user by username
        user = mongo.db.users.find_one({'username': username})
        if user and check_password_hash(user['password'], password):
            session['username'] = username
            flash('Login successful!', 'success')  # Flash success message
            return redirect(url_for('dashboard'))  # Redirect to dashboard
        else:
            flash('Invalid username or password. Please try again.', 'danger')  # Flash error message
            return redirect(url_for('login'))  # Redirect back to login

    return render_template('login.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html')
    return redirect(url_for('login'))

# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)