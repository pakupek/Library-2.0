import sqlite3

connection = sqlite3.connect('library.db')

cur = connection.cursor()

with open('schema_db.sql', 'r') as sql_file:
    connection.executescript(sql_file.read())

book_table = """CREATE TABLE IF NOT EXISTS Book_available (
    id INTEGER AUTOINCREMENT foreign_key=True,
    title varchar(40), 
    book_type STRING, 
    prod_year STRING, 
    author STRING, 
    descrip STRING
)"""
author_table = """CREATE TABLE IF NOT EXISTS Author(
    id INTEGER AUTOINCREMENT primary_key=True,
    first_name varchar(20), 
    last_name varchar(20), 
    born_date STRING, 
    bibliography STRING
)"""
loans_table = """CREATE TABLE IF NOT EXISTS Loans(
    id INTEGER AUTOINCREMENT foreign_kaey=True,
    book STRING, 
    book_type STRING, 
    author STRING, 
    loan_start STRING, 
    loan_end STRING
)"""


connection.commit()
connection.close()