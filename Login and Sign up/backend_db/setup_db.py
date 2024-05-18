from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Adjusted relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.LargeBinary(60), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(10))
    birthday = db.Column(db.String(10))
    phone = db.Column(db.String(15))
    reviews = db.relationship('Review', back_populates='user', cascade="all, delete-orphan")
    posts = db.relationship('Post', back_populates='user', cascade="all, delete-orphan")
    comments = db.relationship('Comment', back_populates='user', cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("length(username) >= 3", name="username_min_length"),
        CheckConstraint("length(password) >= 6", name="password_min_length"),
        CheckConstraint("length(phone) >= 10 and length(phone) <= 15", name="phone_length"),
    )

    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', address):
            raise ValueError("Provided email is not a valid email address")
        return address

    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return username

    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        return password

    @validates('phone')
    def validate_phone(self, key, phone):
        if not re.match(r'^\+?1?\d{9,15}$', phone):
            raise ValueError("Phone number must be between 10 and 15 digits")
        return phone

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

    __table_args__ = (
        CheckConstraint("rating >= 1 and rating <= 5", name="valid_rating"),
    )

    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")

    @validates('title')
    def validate_title(self, key, title):
        if not title:
            raise ValueError("Title cannot be empty")
        return title

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Content cannot be empty")
        return content

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    @validates('content')
    def validate_content(self, key, content):
        if not content:
            raise ValueError("Comment content cannot be empty")
        return content

def setup_database():
    with app.app_context():
        db.create_all()
        print("Database initialized successfully.")

if __name__ == "__main__":
    setup_database()
