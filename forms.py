from wtforms import Form, FileField
from wtforms import StringField, SelectField
from wtforms import PasswordField
from wtforms.fields import EmailField, TextAreaField

from wtforms import validators

class userData(Form):
	username = StringField("Nombre de usuario",
				
				[
				  validators.DataRequired(message="El username es requerido"),	
				  validators.length(min=4, max=25, message="Ingrese un username valido")
				]
				)
	email = EmailField("Email",
			[
			 validators.DataRequired(message="El correo es requerido"),	
			 validators.Email(message="Ingrese un Email valido")
			])
	password = PasswordField("Contraseña",
				[
				 validators.DataRequired(message="La contraseña es requerida"),	
				 validators.length(min=8, max=16, message="Ingrese una contraseña valida")
				]
				)



class LoginForm(Form):
	username = StringField("Nombre de usuario",
				[
				  validators.DataRequired(message="El username es requerido"),	
				  validators.length(min=4, max=25, message="Ingrese un username valido")
				]
				)

	password = PasswordField("Contraseña",
				[
				 validators.DataRequired(message="La contraseña es requerida"),	
				 validators.length(min=8, max=16, message="Ingrese una contraseña valida")
				]
				)

class PostForm(Form):
	nombreObra = StringField("Nombre de la obra",
				[
				 validators.DataRequired(message="Este campo no puede estar vacio")
				]
				)
	nombreAutor = StringField("Nombre del autor",
				[
				 validators.DataRequired(message="Este campo no puede estar vacio")
				]
				)
	text = TextAreaField("Reseña historica",
				[
				 validators.DataRequired(message="Este campo no puede estar vacio"),
				 validators.length(min=8, max=100000)
				]
				
				)