from flask import Blueprint
from flask import render_template, redirect, url_for
from flask import request, flash 
from flask import session
from models.models import User
from models.models import Post
from utils.db import db
from werkzeug.utils import secure_filename
import forms
import app
import os
import uuid


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'jfif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1 )[1].lower() in ALLOWED_EXTENSIONS

arts = Blueprint("arts", __name__)

@arts.route("/home", methods=["GET", "POST"])
def home():

    miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).all()

    return render_template("home.html", miniatura = miniatura)

@arts.route("/")
def index():
    return redirect("/home")

@arts.route("/buscar")
def buscar():
    if request.method == "GET":
        estiloObra = request.args.get("estiloObra")
        generoObra = request.args.get("generoObra")
        nombreObra = request.args.get("cuadroBusqueda")

        #Si no se coloca ningun filtro
        if estiloObra == "" and generoObra == "" and nombreObra == "":
            return redirect("/home")

        #Si solo se busca por estilo de la obra
        elif estiloObra != "" and generoObra == "" and nombreObra == "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.estiloObra == estiloObra).all()
            if miniatura == []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)

        #Si solo se busca por el genero de la obra
        elif estiloObra == "" and generoObra != "" and nombreObra == "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.generoObra == generoObra).all()
            if miniatura == []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)

        #Si solo se busca por el nombre de la obra
        elif estiloObra == "" and generoObra == "" and nombreObra != "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.nombreObra.like(f"%{nombreObra}%")).all()
            if miniatura == []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)

        #Si se busca por los tres filtros
        elif estiloObra != "" and generoObra != "" and nombreObra != "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.estiloObra == estiloObra,
                        Post.generoObra == generoObra,
                        Post.nombreObra.like(f"%{nombreObra}%")).all()
            if miniatura == []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)

        #Si se busca por estilo y genero
        elif estiloObra != "" and generoObra != "" and nombreObra == "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.estiloObra == estiloObra,
                        Post.generoObra == generoObra).all()
            print(miniatura)
            if miniatura == []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)


        #Si se busca por los estilo y nombre
        elif estiloObra != "" and generoObra == "" and nombreObra != "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.estiloObra == estiloObra,
                        Post.nombreObra.like(f"%{nombreObra}%")).all()
            if miniatura is []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)


        #Si se busca por genero y nombre
        elif estiloObra == "" and generoObra != "" and nombreObra != "":
            miniatura = Post.query.with_entities(Post.nombreImagen, Post.nombreObra, Post.id).filter(Post.generoObra == generoObra,
                        Post.nombreObra.like(f"%{nombreObra}%")).all()
            if miniatura is []:
                flash("No se encontraron resultados", "error")
            return render_template("home.html", miniatura = miniatura)


@arts.route("/sign_in", methods=["GET", "POST"])
def new():
    val = forms.userData(request.form)
    if request.method == "POST" and val.validate():
        username = val.username.data
        email = val.email.data
        password = val.password.data

        if User.query.filter_by(username = username).first(): 
            print(User.query.filter_by(username = username).first())
            flash("El nombre de usuario ya esta registrado", "error")
            return redirect("/sign_in") 

        elif User.query.filter_by(email = email).first():
            print(User.query.filter_by(email = email).first()) 
            flash("El correo ya esta registrado", "error")
            return redirect("/sign_in")


        else: 
            new_user = User(username, email, password)

            db.session.add(new_user)
            db.session.commit()
            return redirect( url_for("arts.login") )

    return render_template("sign_in.html", form=val)


#Ruta para el login
@arts.route("/login", methods=["GET", "POST"])
def login():
    login_form = forms.LoginForm(request.form) #Instanciar la clase LoginForm que contiene las validaciones
    if request.method == "POST" and login_form.validate(): #Verificar el tipo de peticion y que las validaciones esten correctas
        #Extraer la informacion del modelo LoginForm
        username = login_form.username.data 
        password = login_form.password.data
        user = User.query.filter_by(username = username).first() #Buscar al usuario en la BD
        if user is not None and password == user.password:
            session['username'] = username
            session["user_id"] = user.id
            return redirect( url_for("arts.home"))

        else:
            auth_error = "Usuario o contraseña incorrecta"
            flash(auth_error, "error")
            return redirect("login")
    return render_template("login.html", form = login_form)



@arts.route("/profile", methods=["GET","POST"])
def profile():
    if 'username' not in session:
        return redirect( url_for("arts.login"))
    
    else:
        username = session['username']
        user_id = session['user_id']
        user = User.query.filter_by(username = username).first()
        posts = Post.query.filter_by(user_id = user_id).all()
        return render_template("profile.html", data=user, posts = posts)


@arts.route("/new_post", methods=["GET", "POST"])
def new_post():
    if 'username' not in session:
        message = "Debe iniciar sesion para crear un post"
        flash(message, "error")
        return redirect( url_for("arts.new"))

    else:
        post = forms.PostForm(request.form)
        username = session['username']
        if request.method == "POST" and post.validate():
            file = request.files["file"]
            estiloObra = request.form["estilo"]
            generoObra = request.form["genero"]
            text = post.text.data
            nombreObra = post.nombreObra.data
            nombreAutor = post.nombreAutor.data
            archivo = secure_filename(file.filename)
            user_id = session["user_id"]
            print(allowed_file(archivo))
            if allowed_file(archivo): 
                nombreImagen = str(uuid.uuid4()) + ".png"
                filepath = os.path.join(app.app.config['UPLOAD_FOLDER'], nombreImagen)
                file.save(filepath)
                queryPost = Post(user_id, text, nombreObra, nombreAutor, nombreImagen, estiloObra, generoObra)
                db.session.add(queryPost)
                db.session.commit()
                return redirect( url_for("arts.home") )
            else:
                flash("Archivo no admitido", "error")
                return redirect("/new_post")
        return render_template("new_post.html", form = post)

@arts.route("/logout")
def logout():
    if 'username' in session:
        session.pop("username")
        flash("Sesion cerrada correctamente", "success")
        return redirect("/home")

    return redirect("/home")

@arts.route("/post/<id>")
def post(id):
    info = Post.query.filter_by(id = int(id)).first()
    return render_template("post.html", info = info)

    
@arts.route("/delete/<id>")
def delete(id):
    post = Post.query.get(int(id))
    db.session.delete(post)
    db.session.commit()
    return redirect("/profile")