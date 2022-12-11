from . import db, login_manager
from werkzeug.security import generate_password_hash
from flask_login import UserMixin

class Contacts(db.Model):
	__tablename__ = "contacts"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), unique=False, nullable=True)
	email = db.Column(db.String(40), unique=False, nullable=True)
	phone = db.Column(db.String(15), unique=False, nullable=True)
	subject = db.Column(db.String(15), unique=False, nullable=True)
	message = db.Column(db.Text, unique=False, nullable=True)

	def __repr__(self):
		return f"Name : {self.name}, Email: {self.email}"

@login_manager.user_loader
def user_loader(user_id):
	return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	__tablename__ = "users"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(15), unique=False, nullable=True)
	email = db.Column(db.String(40), unique=False, nullable=True)
	image_file = db.Column(db.String(40), unique=False, nullable=False, default = 'default.jpg')
	password = db.Column(db.String(60), unique=False, nullable=False)

	def __init__(self, name, email, password):
		self.name = name
		self.email = email
		self.password = generate_password_hash(password)

	def __repr__(self):
		return f"User('{self.name}', '{self.email}')"
