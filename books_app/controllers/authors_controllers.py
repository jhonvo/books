from books_app import app
from flask import Flask, render_template, redirect, session, request
from books_app.models.authors import Author
from books_app.models import books

@app.route('/')
def home():
    return redirect ('/authors')

@app.route('/authors', methods=['GET','POST'])
def authorslist():
    authors = Author.allauthors()
    return render_template ('authors.html', authors = authors)

@app.route('/author/create', methods=['POST'])
def author_create():
    data = request.form
    print ("This is DATA", data)
    newauthor =  Author.newauthor(data)
    return redirect ('/authors')

@app.route('/author/<int:id>', methods=['GET','POST'])
def author_detail(id):
    authorfav = Author.authorfavorites(id)
    booklist = books.Book.missingbooks(id)
    return render_template ('authorinfo.html', authorfav = authorfav, books = booklist)

@app.route('/author/fav', methods=['POST'])
def author_fav():
    data = request.form
    newfav = Author.newbookfav(data)
    redirecturl = f"/author/{data['author_id']}"
    return redirect (redirecturl)

