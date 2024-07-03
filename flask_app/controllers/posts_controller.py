from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

#Importamos los modelos
from flask_app.models.post import Post
from flask_app.models.comment import Comment
from flask_app.models.user import User


#Ruta para plantilla de formularios
@app.route("/create_post", methods=["POST"])
def create_post():
    #request.form = {"content" : "contenido publ", "user_id" : 1}
    if not Post.validate_post(request.form):
        return redirect("/dashboard")
    
    Post.save(request.form)
    return redirect("/dashboard")


@app.route("/delete_post/<int:id>")
def delete_post(id):
    #Metodo que borra un registro en base a su ID
    dicc = {"id" : id}
    Post.delete(dicc)
    return redirect("/dashboard")
    
# Ruta para poder mostrar comentarios dentro de un post..