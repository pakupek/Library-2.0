import sqlite3
from flask import Flask, flash, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    connection = sqlite3.connect('library.db')
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/')
def home():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM Book_available').fetchall()
    connection.close()
    return render_template('books.html', books=books)


@app.route('/addbook', methods=("GET","POST"))
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        book_type = request.form['type']
        prod_year = request.form['production_year']
        author = request.form['author']
        author_born = request.form['author_born_date']
        author_bibliography = request.form['author_bibliography']
        description = request.form['description']
        if not title:
            flash('Title of book is required')
        elif not book_type:
            flash('Type of book is required')
        elif not prod_year:
            flash('Production year of a book is required')
        elif not author:
            flash('Author of book is required')
        elif not description:
            flash('Description of a book is required')
        else:
            connection = get_db_connection()
            connection.execute('INSERT INTO Book_available (title, book_type, prod_year, author, descrip) VALUES(?, ?, ?, ?, ?)',
                        (title, book_type, prod_year, author, description))
            connection.execute('INSERT INTO Author (first_last_name, born_date, bibliography) VALUES(?, ?, ?)',
                        (author, author_born, author_bibliography))
            connection.commit()
            connection.close()
            return redirect(url_for('home'))
    return render_template('create.html')


if __name__ == "__main__":
    app.run(debug=True)