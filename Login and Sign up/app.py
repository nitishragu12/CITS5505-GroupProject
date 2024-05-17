from flask import Flask, request, redirect, render_template, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../backend_db/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Used for session management

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Adjusted length for bcrypt hash
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.String(10))
    phone = db.Column(db.String(15))

def hash_password(password):
    # Hashes the password and returns a UTF-8 string of the hash
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, user_password):
    # Checks if the hashed password matches the user's password
    return bcrypt.checkpw(user_password.encode(), hashed_password.encode())

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
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/home')
def dashboard():
    return render_template('home.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/back2Home')
def back2Home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
