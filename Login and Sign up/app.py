from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)


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
        password = hash_password(request.form.get('password'))
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        gender = request.form.get('gender')
        birthday = request.form.get('birthday')
        phone = request.form.get('phone')

        if not all([username, password, email, first_name, last_name]):
            flash("Please fill in all required fields")
            return redirect(url_for('signup'))

        new_user = User(username=username, password=password, email=email,
                        first_name=first_name, last_name=last_name, gender=gender,
                        birthday=birthday, phone=phone)

        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error in database operation: {e}")
            return redirect(url_for('signup'))

        flash("Signup successful. Please login.")
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        provided_password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password(user.password, provided_password):
            session['user_id'] = user.id
            flash("Logged in successfully!")
            return redirect(url_for('about'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('faq'))
    return render_template('login.html')



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
