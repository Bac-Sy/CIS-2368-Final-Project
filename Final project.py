import flask
from flask import Flask, request, jsonify, make_response
from datetime import datetime
import hashlib
import creds
from sql import create_connection, execute_query, execute_read_query

# Establish database connection using credentials from creds.py
myCreds = creds.creds()
conn = create_connection(myCreds.constring, myCreds.user, myCreds.password, myCreds.database)

delete_table_statement1 = "DROP TABLE borrowingrecords"
execute_query(conn, delete_table_statement1)

delete_table_statement = "DROP TABLE books"
execute_query(conn, delete_table_statement)

create_books_table = """
 CREATE TABLE IF NOT EXISTS books (
     id INT AUTO_INCREMENT,
     title VARCHAR(255) NOT NULL,
     author VARCHAR(255) NOT NULL,
     genre VARCHAR(100) NOT NULL,
     status VARCHAR(20) NOT NULL,
     PRIMARY KEY (id)
 )
 """

execute_query(conn, create_books_table)

create_borrowingrecords_table = """
 CREATE TABLE IF NOT EXISTS borrowingrecords (
     id INT AUTO_INCREMENT,
     bookid INT NOT NULL,
     customerid INT NOT NULL,
     borrowdate DATE NOT NULL,
     returndate DATE,
     late_fee INT DEFAULT 0,
     FOREIGN KEY (bookid) REFERENCES books(id),
     FOREIGN KEY (customerid) REFERENCES customers(id),
     PRIMARY KEY (id)
 )
 """

# setting up an application name
# app = flask.Flask(__name__) # sets up the app
# app.config["DEBUG"] = True # allow to show errors in the browser


# @app.route('/api/books/add', methods=['POST'])
# def add_book():
#     new_book = request.get_json()
#     query = """
#     INSERT INTO books (title, author, genre, status)
#     VALUES (%s, %s, %s, %s)
#     """
#     values = (
#         new_book['title'],
#         new_book['author'],
#         new_book['genre'],
#         new_book['status']
#     )
#     execute_query(conn, query, values)
#     return make_response(jsonify({"message": "Book added successfully"}), 200)

# # Shows all books in the database
# @app.route('/api/books/inventory', methods=['GET'])
# def list_books():
#     query = "SELECT * FROM books"
#     books = execute_read_query(conn, query)
#     return jsonify(books)

# # Updates the book by ID
# @app.route('/api/books/update', methods=['PUT'])
# def update_book():
#     data = request.get_json()
#     book_id = data.get('id')
#     if not book_id:
#         return make_response(jsonify({"message": "Book ID is required"}), 400)
#     query = """
#     UPDATE books
#     SET title = %s, author = %s, genre = %s, status = %s
#     WHERE id = %s
#     """
#     values = (
#         data['title'],
#         data['author'],
#         data['genre'],
#         data['status'],
#         book_id
#     )
#     execute_query(conn, query, values)
#     return make_response(jsonify({"message": "Book updated successfully"}), 200)




#app.run()