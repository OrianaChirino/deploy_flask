from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#Importamos los modelos
from flask_app.models.user import User
from flask_app.models.post import Post

#Importar Bcrypt
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

#Ruta para plantilla de formularios
@app.route("/")
def index():
    return render_template("index.html")

#Ruta que recibe el formulario
@app.route("/register", methods=["POST"])
def register():
    #request.form = {"first_name": "Elena", "last_name": "De Troya"....}

    #Validar la info que recibimos
    if not User.validate_user(request.form):
        #No es valida la info, redirecciono al form
        return redirect("/")


    #Encriptar o Hashear contraseña
    pass_hash = bcrypt.generate_password_hash(request.form["password"])

    #Crear un diccionario que simule el form incluyendo la contraseña hasheada
    form = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": pass_hash
    }

    id = User.save(form) #recibo el id del nuevo usuario 1
    session["user_id"] = id
    session["first_name"] = request.form["first_name"]
    return redirect("/dashboard")

#Ruta que recibe el formulario
@app.route("/dashboard")
def dashboard():
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        return redirect("/")
    dicc = {"id" : session['user_id']}
    user = User.get_by_id(dicc) #Ontener el objeto User
    
    #Enviar todas las publicaciones
    posts = Post.get_all()
    return render_template("dashboard.html", user = user, posts = posts)
 


@app.route("/login", methods=["POST"])
def login():
    #request.form = {"email": "elena@codingdojo.com", "password": "Hola123"}
    #Verifico que el email esté en mi BD
    user = User.get_by_email(request.form) #Recibo false si no existe ese usuario en mi BD o recibo un objeto de usuario con la info guardada en la BD

    if not user: #Si user es igual a Falso, es decir, que no existe...
        flash("Email not found", "login")
        return redirect("/")
    #Si user SI es objeto User...
    #user = User() .id=1, .first_name="Elena", .last_name="De Troya"... .password=#"g2&r&tfd$657%$7u$3"
    if not bcrypt.check_password_hash(user.password, request.form["password"]):  #entre los parentesis pongo el password hasheado, y el password NO hasheado
        flash("Password incorrect", "login")
        return redirect("/")
    
    session["user_id"] = user.id
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")