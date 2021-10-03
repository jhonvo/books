from flask.globals import request
from books_app import app
from books_app.config.mysqlconnection import connectToMySQL
from books_app.models import books

class Author:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.books = []

    @classmethod
    def newauthor(cls,data):
        query = "INSERT INTO authors (name) VALUE (%(name)s)"
        results = connectToMySQL("mydb").query_db(query,data)
        return results

    @classmethod
    def allauthors(cls):
        query = "SELECT * FROM authors;"
        results = connectToMySQL("mydb").query_db(query)
        authors = []
        for line in results:
            authors.append(Author(line))
        return authors

    @classmethod
    def missingauthors(cls,id):
        query = "SELECT * FROM authors WHERE authors.id NOT IN (SELECT DISTINCT id FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id WHERE favorites.book_id = %(id)s);"
        data = {
            'id' : id
        }
        results = connectToMySQL("mydb").query_db(query,data)
        authors = []
        for line in results:
            authors.append(Author(line))
        return authors

    @classmethod
    def authorfavorites(cls,id):
        query = "SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;"
        data = {
            'id' : id
        }
        results = connectToMySQL("mydb").query_db(query,data)
        author = Author(results[0])
        for results_line in results:
            bookdata = {
                'id' : results_line['books.id'],
                'title' : results_line['title'],
                'num_of_pages' : results_line['num_of_pages']
            }
            author.books.append(books.Book(bookdata))
        return author

    @classmethod
    def newbookfav(cls,data):
        query = "INSERT INTO favorites (author_id, book_id) VALUES (%(author_id)s,%(book_id)s);"
        results = connectToMySQL("mydb").query_db(query,data)
        return results


