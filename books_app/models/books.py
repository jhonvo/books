from books_app import app
from books_app.config.mysqlconnection import connectToMySQL
from books_app.models import authors

class Book:
    def __init__(self,data):
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.authors = []

    @classmethod
    def allbooks(cls):
        query = "SELECT * FROM books;"
        results = connectToMySQL("mydb").query_db(query)
        books = []
        for line in results:
            books.append(Book(line))
        return books

    @classmethod
    def missingbooks(cls,id):
        query = "SELECT * FROM books WHERE books.id NOT IN (SELECT DISTINCT id FROM books LEFT JOIN favorites ON books.id = favorites.book_id WHERE favorites.author_id = %(id)s);"
        data = {
            'id' : id
        }
        results = connectToMySQL("mydb").query_db(query,data)
        books = []
        for line in results:
            books.append(Book(line))
        return books

    @classmethod
    def newbook(cls, data):
        query = "INSERT INTO books (title,num_of_pages) VALUES (%(title)s,%(num_of_pages)s);"
        results = connectToMySQL("mydb").query_db(query,data)
        return results

    @classmethod
    def bookfavorites(cls, id):
        query = "SELECT * FROM books LEFT JOIN favorites ON books.id = favorites.book_id LEFT JOIN authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;"
        data = {
            'id' : id
        }
        results = connectToMySQL("mydb").query_db(query,data)
        print ("RESULTS", results)
        book = Book(results[0])
        for results_line in results:
            author_data = {
                'id' : results_line['authors.id'],
                'name' : results_line['name']
            }
            book.authors.append(authors.Author(author_data))
        return book
