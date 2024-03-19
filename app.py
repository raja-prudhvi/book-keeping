
#DB_USER=your_username DB_PASSWORD=your_password DB_HOST=book-keeping-db DB_PORT=5432 DB_NAME=your_database_name python3 app.py

from flask import Flask, render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Read database credentials from environment variables
db_user = os.environ.get('DB_USER', 'your_username')
db_password = os.environ.get('DB_PASSWORD', 'your_password')
db_host = os.environ.get('DB_HOST', 'db_host')
db_port = os.environ.get('DB_PORT', '5432')
db_name = os.environ.get('DB_NAME', 'your_database_name')

# Configure SQLAlchemy database URI
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

@app.route('/')
def index():
    books = Book.query.all()
    return render_template('index.html', books=books)

@app.route('/add_book', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    new_book = Book(title=title, author=author)
    db.session.add(new_book)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/update_book/<int:id>', methods=['GET', 'POST'])
def update_book(id):
    book = Book.query.get_or_404(id)
    if request.method == 'POST':
        book.title = request.form.get('title')
        book.author = request.form.get('author')
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update.html', book=book)

@app.route('/delete_book/<int:id>', methods=['POST'])
def delete_book(id):
    book = Book.query.get_or_404(id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

