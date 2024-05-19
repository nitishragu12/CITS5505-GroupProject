from flask import Flask, request, redirect, render_template, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../backend_db/instance/app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    posts = db.relationship('Post', back_populates='user', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='user', cascade="all, delete-orphan")

    def get_average_rating(self):
        if not self.reviews:
            return 0
        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500))
    user = db.relationship('User', back_populates='reviews')

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

def check_password(hashed_password, user_password):
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
            session['first_name'] = user.first_name
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

@app.route('/review', methods=['GET', 'POST'])
def review():
    if request.method == 'POST':
        user_id = request.form.get('person')
        rating = request.form.get('rating')
        feedback = request.form.get('feedback')

        if not all([user_id, rating, feedback]):
            flash("Please fill in all fields")
            return redirect(url_for('review'))

        new_review = Review(user_id=user_id, rating=int(rating), feedback=feedback)

        db.session.add(new_review)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            flash(f"Error in database operation: {e}")
            return redirect(url_for('review'))

        flash("Review submitted successfully.")
        return redirect(url_for('dashboard'))
    return render_template('review.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

@app.route('/back2Home')
def back2Home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully.")
    return redirect(url_for('home'))

@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_list = [{"id": user.id, "name": f"{user.first_name} {user.last_name}"} for user in users]
    return jsonify(users_list)

@app.route('/api/users/<int:user_id>/average_rating', methods=['GET'])
def get_average_rating(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({"user_id": user_id, "average_rating": user.get_average_rating()})
    else:
        return jsonify({"error": "User not found"}), 404
        
@app.route('/api/posts', methods=['GET', 'POST'])
def handle_posts():
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        user_id = session['user_id']
        title = request.json.get('title')
        content = request.json.get('content')

        if not all([title, content]):
            return jsonify({"error": "Missing title or content"}), 400

        new_post = Post(user_id=user_id, title=title, content=content)

        db.session.add(new_post)
        try:
            db.session.commit()
            return jsonify({"success": "Post created"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error in database operation: {e}"}), 500

    search_query = request.args.get('search')
    if search_query:
        posts = Post.query.filter(Post.title.ilike(f'%{search_query}%')).all()
    else:
        posts = Post.query.all()
    posts_list = [{"id": post.id, "title": post.title, "content": post.content, "username": post.user.username, "user_rating": post.user.get_average_rating()} for post in posts]
    return jsonify(posts_list)

@app.route('/api/posts/<int:post_id>/comments', methods=['GET', 'POST'])
def handle_comments(post_id):
    if request.method == 'POST':
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        user_id = session['user_id']
        content = request.json.get('content')

        if not content:
            return jsonify({"error": "Missing content"}), 400

        new_comment = Comment(user_id=user_id, post_id=post_id, content=content)

        db.session.add(new_comment)
        try:
            db.session.commit()
            return jsonify({"success": "Comment added"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error in database operation: {e}"}), 500

    comments = Comment.query.filter_by(post_id=post_id).all()
    comments_list = [{"content": comment.content, "username": comment.user.username, "user_rating": comment.user.get_average_rating()} for comment in comments]
    return jsonify(comments_list)

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard_data():
    users = User.query.all()
    leaderboard = [{"id": user.id, "name": f"{user.first_name} {user.last_name}", "average_rating": user.get_average_rating()} for user in users]
    leaderboard.sort(key=lambda x: x['average_rating'], reverse=True)
    return jsonify(leaderboard)

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
