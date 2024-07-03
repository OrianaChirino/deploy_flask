from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es e encargado de mostrar los mensajes

import re  # Expresiones Regulares -> Empatar con un patrón de texto
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class User:
    def __init__(self, data):
        #data = diccionario que tiene toda la info para el objeto
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

#OJO AQUI! las @classmethod siembre deben ir indentadas dentro de la clase!!!
    #Metodo que crea un nuevo objeto de Usuario
    @classmethod
    def save(cls, form):
        #form = {"first_name":"Elena", "last_name":"De Troya", "email":"elena@cd.com", "password":"YA ESTÁ HASHEADO"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        return connectToMySQL('esquema_foro_publicaciones').query_db(query, form) #Regresa el id del nuevo registro
    
    #Metodo que regresa objeto de Usuario en base a email
    @classmethod
    def get_by_email(cls, form):
        #form = {"email":"elena@cd.com", "password":"hola123"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_foro_publicaciones').query_db(query, form) #Regresa Lista de Diccionario

        if len(result) < 1: #Revisa si mi lista esté vacía
            return False
        else:
            #Me regresa 1 registro
            #result = [{"id":1, "first_name":"Elena"....}]
            user = cls(result[0]) #User ({"id":1, "first_name":"Elena"....})
            return user
        
         #Metodo que regresa objeto de Usuario en base a email
    @classmethod
    def get_by_id(cls, data):
        #form = {"id": 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_foro_publicaciones').query_db(query, data) #Regresa Lista de Diccionario
        user = cls(result[0])
        return user

    @staticmethod  #es static porque es un metodo que ayuda a hacer una validacion
    def validate_user(form):
        #form = {diccionario con toda la info del formulario}
        is_valid = True    

        #Validamos que el nombre tenga al menos dos caracteres
        if len(form["first_name"]) < 2:
            flash("First name must have at least 2 chars", "register")
            is_valid = False

        #Validamos que el apellido tenga al menos dos caracteres
        if len(form["last_name"]) < 2:
            flash("Last name must have at least 2 chars", "register")
            is_valid = False

        #Validamos que el largo del password tenga al menos 6 caracteres
        if len(form["password"]) < 6:
            flash("Password must have at least 6 chars", "register")
            is_valid = False

        #Validamos que el email sea único
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_foro_publicaciones').query_db(query, form) #Regresa Lista de Diccionario
        #Aqui podría ocurrir que me regrese una lista vacía o una lista con 1 diccionario
        if len(result) >=1:
            #Si existe ese email en mi Base de datos
            flash("Email already registered", "register")
            is_valid = False

        #Validamos que las coontraseñas coinsidan (porque tengo el campo password y el campo confirm password)
        if form["password"] != form["confirm"]:
            flash("Password do not match", "register")
            is_valid = False

        #Validamos que el email cumpla con la expresion regular
        if not EMAIL_REGEX.match(form["email"]):
            flash("Email not valid", "register")
            is_valid = False
        
        return is_valid