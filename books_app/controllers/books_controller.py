from books_app import app
from flask import Flask, render_template, redirect, request, session
from books_app.models import authors
from books_app.models.books import Book

@app.route('/books', methods=['GET','POST'])
def bookslist():
    books = Book.allbooks()
    print ("BOOKS", books[0].id)
    return render_template ('books.html', books = books)

@app.route('/book/create', methods=['POST'])
def book_create():
    data = request.form
    newbook = Book.newbook(data)
    return redirect ('/books')

@app.route('/book/<int:id>', methods=['GET','POST'])
def book_detail(id):
    bookfav = Book.bookfavorites(id)
    authorlist = authors.Author.allauthors()
    return render_template ('bookinfo.html', bookfav = bookfav, authors = authorlist)

@app.route('/book/fav', methods=['POST'])
def book_fav():
    data = request.form
    newfav = authors.Author.newbookfav(data)
    redirecturl = f"/book/{data['book_id']}"
    return redirect (redirecturl)