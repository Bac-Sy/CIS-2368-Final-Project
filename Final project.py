import flask
from flask import Flask, request, jsonify, make_response
from datetime import datetime
import hashlib
import creds
from sql import create_connection, execute_query, execute_read_query

# Establish database connection using credentials from creds.py
myCreds = creds.creds()
conn = create_connection(myCreds.constring, myCreds.user, myCreds.password, myCreds.database)

# setting up an application name
app = flask.Flask(__name__) # sets up the app
app.config["DEBUG"] = True # allow to show errors in the browser


# Add a new book to the database
@app.route('/api/books/add', methods=['POST'])
def add_book():
    new_book = request.get_json()
    query = """
    INSERT INTO books (title, author, genre, status)
    VALUES (%s, %s, %s, %s)
    """
    values = (
        new_book['title'],
        new_book['author'],
        new_book['genre'],
        new_book.get('status', 'available')  # defaults to 'available' if not provided
    )
    execute_query(conn, query, values)
    return make_response(jsonify({"message": "Book added successfully"}), 200)


app.run()