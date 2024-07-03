from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash #flash es e encargado de mostrar los mensajes

class Comment:
    def __init__(self, data):
        #data = {diccionario con la info de mi BD}
        self.id = data["id"]
        self.content = data["content"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.post_id = data["post_id"]
        self.user_id = data["user_id"]

        self.user_name = data["user_name"]

    @classmethod
    def save(cls, form):
        #form = {"content" : "contenido de la publicacion", "user_id" : 1}
        query = "INSERT INTO comments (content, post_id, user_id) VALUES (%(content)s, %(post_id)s, %(user_id)s)"
        return connectToMySQL("esquema_foro_publicaciones").query_db(query, form)
    
    @staticmethod
    def validate_comment(form):
        is_valid = True

        if len(form["content"]) < 1:
            flash("Comment content is required", "comment")
            is_valid = False
        return is_valid    

    #Metodo para obtener los comentarios de un Post
    @classmethod
    def get_by_post_id(cls, post_id):
        query = """
                SELECT users.first_name, comments.created_at, comments.content
                FROM comments
                JOIN users ON comments.user_id = users.id
                WHERE comments.post_id = %(post_id)s
                """
        results = connectToMySQL("esquema_foro_publicaciones").query_db(query, (post_id))
        return results
  