from utils.db import db
import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(100))
	password = db.Column(db.String(20))
	post = db.relationship("Post")

	def __init__(self, username, email, password):
		self.username = username
		self.email = email
		self.password = password

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey("user.id") )
	nombreAutor = db.Column(db.String(40))
	nombreObra = db.Column(db.String(40))
	nombreImagen = db.Column(db.String(60))
	text = db.Column(db.Text())
	estiloObra = db.Column(db.String(30))
	generoObra = db.Column(db.String(30))
	created_date = db.Column(db.DateTime, default=datetime.datetime.now)

	def __init__(self, user_id, text, nombreObra, nombreAutor, nombreImagen, estiloObra, generoObra):
		self.text = text
		self.nombreObra = nombreObra
		self.nombreAutor = nombreAutor 
		self.user_id = user_id
		self.nombreImagen = nombreImagen
		self.estiloObra = estiloObra
		self.generoObra = generoObra
