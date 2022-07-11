import sqlite3
from flask import Flask, flash, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

#Connection with database
def get_db_connection():
    connection = sqlite3.connect('library.db')
    connection.row_factory = sqlite3.Row
    return connection

#Homepage
@app.route('/')
def home():
    connection = get_db_connection()
    books = connection.execute('SELECT * FROM Book_available').fetchall()
    connection.close()
    return render_template('books.html', books=books)

#Site with authors table
@app.route('/authors')
def authors_database():
    connection = get_db_connection()
    authors = connection.execute('SELECT *FROM Author').fetchall()
    connection.close()
    return render_template('authors.html', authors=authors)

#Place where you can add a book 
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
    else:
        return render_template('create.html')

#Place where you can add a loan 
@app.route('/addloan', methods=("GET","POST"))
def add_loan():
    if request.method == 'POST':
        title = request.form['title']
        book_type = request.form['type']
        author = request.form['author']
        loan_start = request.form['loan_start']
        loan_end = request.form['loan_end']
     
        connection = get_db_connection()
        cur = connection.cursor()
  
        
        #Checking if entered title is in Book_available
        cur.execute("SELECT * FROM Book_available WHERE title=?", (title,))
        result = cur.fetchall()
        
        if result is not None :
            for row in result:
                if row[5] == 'available':
                    cur.execute('INSERT INTO Loans (book, book_type, author, loan_start, loan_end) VALUES(?, ?, ?, ?, ?)',
                        (title, book_type, author, loan_start, loan_end))
                    cur.execute('UPDATE Book_available SET STATUS=? WHERE title=?',(str('loaned'),row[1]))
                    connection.commit()
                    connection.close()
                    return redirect(url_for('home'))
                
                elif row[5] == 'loaned':
                    flash('Selected book is loaned')

        else:
            flash('Selected book is not available in our library')
            return redirect(url_for('home'))
    else:
        return render_template('addloan.html')          

@app.route('/loans')
def loans():
    connection = get_db_connection()
    loans = connection.execute('SELECT * FROM Loans').fetchall()
    connection.close()
    return render_template('loans.html', loans=loans)



if __name__ == "__main__":
    app.run(debug=True)