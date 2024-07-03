from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app

# Importamos los modelos
from flask_app.models.comment import Comment
from flask_app.models.post import Post  # Importar el modelo Post

@app.route('/posts/<int:post_id>/comments', methods=['POST'])
def create_comment(post_id):
    if 'user_id' not in session:
        return redirect('/')

    if not Comment.validate_comment(request.form):
        return redirect('/dashboard')

    data = {
        'content': request.form['content'],
        'post_id': post_id,  # Obtener post_id de la ruta
        'user_id': session['user_id']
    }

    Comment.save(data)
    return redirect('/dashboard')


