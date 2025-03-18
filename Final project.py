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

delete_table_statement2 = "DROP TABLE books"
execute_query(conn, delete_table_statement2)

delete_table_statement = "DROP TABLE customers"
execute_query(conn, delete_table_statement)