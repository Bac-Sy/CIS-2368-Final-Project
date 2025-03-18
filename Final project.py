import flask
from flask import Flask, request, jsonify, make_response
from datetime import datetime
import hashlib
import creds
from sql import create_connection, execute_query, execute_read_query

# Establish database connection using credentials from creds.py
myCreds = creds.creds()
conn = create_connection(myCreds.constring, myCreds.user, myCreds.password, myCreds.database)


create_books_table = """
CREATE TABLE IF NOT EXISTS books (
    id INT AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    genre VARCHAR(100),
    status VARCHAR(20) DEFAULT 'available',
    PRIMARY KEY (id)
)
"""
execute_query(conn, create_books_table)

create_customers_table = """
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT,
    firstname VARCHAR(100),
    lastname VARCHAR(100),
    email VARCHAR(255) UNIQUE,
    passwordhash VARCHAR(64),
    PRIMARY KEY (id)
)
"""
execute_query(conn, create_customers_table)

create_borrowingrecords_table = """
CREATE TABLE IF NOT EXISTS borrowingrecords (
    id INT AUTO_INCREMENT,
    bookid INT,
    customerid INT,
    borrowdate DATE,
    returndate DATE,
    late_fee DECIMAL(10,2) DEFAULT 0,
    FOREIGN KEY (bookid) REFERENCES books(id),
    FOREIGN KEY (customerid) REFERENCES customers(id),
    PRIMARY KEY (id)
)
"""
execute_query(conn, create_borrowingrecords_table)