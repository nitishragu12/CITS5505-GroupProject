from flask import Flask, request, redirect, render_template, url_for

import sqlite3
import hashlib

app = Flask(__name__, static_url_path='/static')



def get_db_connection():
    conn = sqlite3.connect('../backend_db/app.db')  
    return conn

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')

        # Check all required fields are filled
        if not all([username, password, email, first_name, last_name]):
            return "Please fill in all required fields", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO users (username, password, email, first_name, last_name, gender, birthday, phone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                           (username, password, email, first_name, last_name, gender, birthday, phone))
            conn.commit()
        except sqlite3.IntegrityError as e:
            conn.rollback()
            return f"Error in database operation: {e}", 400
        finally:
            conn.close()

        return redirect(url_for('login'))  # Assume there's a 'login' view to redirect to
    return render_template('signup.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.sha256(request.form['password'].encode()).hexdigest()

        conn = sqlite3.connect('../backend_db/app.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            return "Logged in successfully!"  # This would be the place to set up session management in a real app
        else:
            return "Login failed, check your username and password."
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=True)
