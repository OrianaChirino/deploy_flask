from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es e encargado de mostrar los mensajes

#Importo Comment
from flask_app.models.comment import Comment

class Post:
    def __init__(self, data):
        #data = {diccionario con la info de mi BD}
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]

        self.user_name = data["user_name"]
        self.comments = []

    @classmethod
    def save(cls, form):
        #form = {"content" : "contenido de la publicacion", "user_id" : 1}
        query = "INSERT INTO posts (content, user_id) VALUES (%(content)s, %(user_id)s)"
        return connectToMySQL("esquema_foro_publicaciones").query_db(query, form)
    
    @staticmethod
    def validate_post(form):
        is_valid = True

        if len(form["content"]) < 1:
            flash("Post content is required", "post")
            is_valid = False
        return is_valid    

    @classmethod
    def get_all(cls):
        query = "SELECT posts.*, users.first_name as user_name FROM posts JOIN users ON posts.user_id = users.id ORDER BY created_at DESC;"
        results = connectToMySQL("esquema_foro_publicaciones").query_db(query)
        posts = []
        for p in results:
            #Creo el objeto de post primero
            post = cls(p)
            #Genero una consulta en la cual vaya específicamente por los comments del post
            query_comments = "SELECT comments.*, users.first_name as user_name FROM comments JOIN users ON comments.user_id = users.id WHERE post_id = %(post_id)s"
            data_comment = {"post_id": p["id"]} #genero un diccionario para hacer la consulta, que incluya el id del post
            results_comments = connectToMySQL("esquema_foro_publicaciones").query_db(query_comments, data_comment)
            comments = [] #Lista de comments vacía
            for c in results_comments:
                comments.append(Comment(c)) #Creo objeto de comment y lo agrego a la lista
            post.comments = comments #atributo comments de post lo igualo a la lista de comentarios

            posts.append(post) #1.- cls(p): Genera el objeto de publicación con el diccionario    2.- append agrega el objeto a la lista de posts
        return posts

    @classmethod
    def delete(cls, data):
        #data = {"id": 2}
        query = "DELETE FROM posts WHERE id = %(id)s"
        connectToMySQL("esquema_foro_publicaciones").query_db(query, data)


