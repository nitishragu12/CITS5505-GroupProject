from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates  # Importing validator decorator
from sqlalchemy import CheckConstraint  # Importing CheckConstraint for table constraints
import re  # Importing regex module

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'  # Adjusted relative path
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model for database
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
        CheckConstraint("length(username) >= 3", name="username_min_length"),  # Username minimum length constraint
        CheckConstraint("length(password) >= 6", name="password_min_length"),  # Password minimum length constraint
        CheckConstraint("length(phone) >= 10 and length(phone) <= 15", name="phone_length"),  # Phone number length constraint
    )

    # Validator for email field
    @validates('email')
    def validate_email(self, key, address):
        if not re.match(r'[^@]+@[^@]+\.[^@]+', address):  # Regex pattern for email validation
            raise ValueError("Provided email is not a valid email address")
        return address

    # Validator for username field
    @validates('username')
    def validate_username(self, key, username):
        if len(username) < 3:  # Minimum username length constraint
            raise ValueError("Username must be at least 3 characters long")
        return username

    # Validator for password field
    @validates('password')
    def validate_password(self, key, password):
        if len(password) < 6:  # Minimum password length constraint
            raise ValueError("Password must be at least 6 characters long")
        return password

    # Validator for phone field
    @validates('phone')
    def validate_phone(self, key, phone):
        if not re.match(r'^\+?1?\d{9,15}$', phone):  # Regex pattern for phone number validation
            raise ValueError("Phone number must be between 10 and 15 digits")
        return phone

    # Method to calculate average rating for the user
    def get_average_rating(self):
        if not self.reviews:
            return 0
        total_rating = sum(review.rating for review in self.reviews)
        return total_rating / len(self.reviews)

# Review model for database
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(500))
    user = db.relationship('User', back_populates='reviews')

    __table_args__ = (
        CheckConstraint("rating >= 1 and rating <= 5", name="valid_rating"),  # Valid rating constraint
    )

    # Validator for rating field
    @validates('rating')
    def validate_rating(self, key, rating):
        if rating < 1 or rating > 5:  # Rating value constraint
            raise ValueError("Rating must be between 1 and 5")
        return rating

# Post model for database
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade="all, delete-orphan")

    # Validator for title field
    @validates('title')
    def validate_title(self, key, title):
        if not title:  # Title should not be empty
            raise ValueError("Title cannot be empty")
        return title

    # Validator for content field
    @validates('content')
    def validate_content(self, key, content):
        if not content:  # Content should not be empty
            raise ValueError("Content cannot be empty")
        return content

# Comment model for database
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user = db.relationship('User', back_populates='comments')
    post = db.relationship('Post', back_populates='comments')

    # Validator for content field
    @validates('content')
    def validate_content(self, key, content):
        if not content:  # Comment content should not be empty
            raise ValueError("Comment content cannot be empty")
        return content

# Function to setup the database
def setup_database():
    with app.app_context():
        db.create_all()  # Creating all database tables
        print("Database initialized successfully.")

# Running the setup_database function when the script is executed
if __name__ == "__main__":
    setup_database()

