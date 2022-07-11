import sqlite3

#Connection with database
connection = sqlite3.connect('library.db')
cur = connection.cursor()

#Creating tables
book_table = """CREATE TABLE Book_available (
    id INTEGER ,
    title varchar(40), 
    book_type STRING, 
    prod_year STRING, 
    author STRING,
    status TEXT DEFAULT 'available',
    descrip STRING
)"""
author_table = """CREATE TABLE Author(
    id INTEGER PRIMARY KEY,
    first_last_name STRING, 
    born_date STRING, 
    bibliography STRING
)"""
loans_table = """CREATE TABLE Loans(
    id INTEGER ,
    book STRING, 
    book_type STRING, 
    author STRING, 
    loan_start STRING, 
    loan_end STRING
)"""

cur.execute(book_table)
cur.execute(author_table)
cur.execute(loans_table)
connection.commit()
connection.close()