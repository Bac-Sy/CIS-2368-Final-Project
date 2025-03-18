import flask
from flask import Flask, request, jsonify, make_response
from datetime import datetime
import hashlib
import creds
from sql import create_connection, execute_query, execute_read_query

# Establish database connection using credentials from creds.py
myCreds = creds.creds()
conn = create_connection(myCreds.constring, myCreds.user, myCreds.password, myCreds.database)

#setting up an application name
app = flask.Flask(__name__) # sets up the app
app.config["DEBUG"] = True # allow to show errors in the browser


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
        new_book['status']
    )
    execute_query(conn, query, values)
    return make_response(jsonify({"message": "Book added successfully"}), 200)

# Shows all books in the database
@app.route('/api/books/inventory', methods=['GET'])
def list_books():
    query = "SELECT * FROM books"
    books = execute_read_query(conn, query)
    return jsonify(books)

@app.route('/api/books/update', methods=['PUT'])
def update_book():
    data = request.get_json()
    book_id = data.get('id')
    if not book_id:
        return make_response(jsonify({"message": "Book ID is required"}), 400)
    query = """
    UPDATE books
    SET title = %s, author = %s, genre = %s, status = %s
    WHERE id = %s
    """
    values = (
        data['title'],
        data['author'],
        data['genre'],
        data['status'],
        book_id
    )
    execute_query(conn, query, values)
    return make_response(jsonify({"message": "Book updated successfully"}), 200)

# Deletes a book by ID
@app.route('/api/books/delete', methods=['DELETE'])
def delete_book():
    data = request.get_json()
    book_id = data.get('id')
    if not book_id:
        return make_response(jsonify({"message": "Book ID is required"}), 400)
    query = "DELETE FROM books WHERE id = %s"
    execute_query(conn, query, (book_id,))
    return make_response(jsonify({"message": "Book deleted successfully"}), 200)

# Adds a new customer to the database
@app.route('/api/customers/add', methods=['POST'])
def add_customer():
    new_customer = request.get_json()
    password = new_customer.get('password')
    if not password:
        return make_response(jsonify({"message": "Password is required"}), 400)
    
    # Hash the password before storing it in the database
    passwordhash = hashlib.sha256(password.encode()).hexdigest()
    query = """
    INSERT INTO customers (firstname, lastname, email, passwordhash)
    VALUES (%s, %s, %s, %s)
    """
    values = (
        new_customer['firstname'],
        new_customer['lastname'],
        new_customer['email'],
        passwordhash
    )
    execute_query(conn, query, values)
    return make_response(jsonify({"message": "Customer added successfully"}), 200)

# Shows all customers in the database
@app.route('/api/customers/inventory', methods=['GET'])
def list_customers():
    query = "SELECT * FROM customers"
    customers = execute_read_query(conn, query)
    return jsonify(customers)

# Deletes a customer by ID
@app.route('/api/customers/delete', methods=['DELETE'])
def delete_customer():
    data = request.get_json()
    customer_id = data.get('id')
    if not customer_id:
        return make_response(jsonify({"message": "Customer ID is required"}), 400)
    query = "DELETE FROM customers WHERE id = %s"
    execute_query(conn, query, (customer_id,))
    return make_response(jsonify({"message": "Customer deleted successfully"}), 200)

# Updates a customer's information
@app.route('/api/customers/update', methods=['PUT'])
def update_customer():
    data = request.get_json()
    customer_id = data.get('id')
    if not customer_id:
        return make_response(jsonify({"message": "Customer ID is required"}), 400)
    query = "UPDATE customers SET firstname = %s, lastname = %s, email = %s"
    values = [
        data['firstname'],
        data['lastname'],
        data['email']
    ]
    # If a new password is provided, hash and update it
    if data.get('password'):
        passwordhash = hashlib.sha256(data.get('password').encode()).hexdigest()
        query += ", passwordhash = %s"
        values.append(passwordhash)
    query += " WHERE id = %s"
    values.append(customer_id)
    execute_query(conn, query, tuple(values))
    return make_response(jsonify({"message": "Customer updated successfully"}), 200)

app.run()