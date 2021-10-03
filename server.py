from flask import Flask, session, render_template, redirect, request
from books_app import app
from books_app.controllers import authors_controllers, books_controller


if __name__ == "__main__":
    app.run(debug=True)