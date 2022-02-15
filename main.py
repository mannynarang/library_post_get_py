from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import sqlite3
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'HELLO_KEY'

# creates database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-books-collection.db"
# creates cursor
db = SQLAlchemy(app)


class editForm(FlaskForm):
    new_rating = StringField('New Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')


class addBookForm(FlaskForm):
    book_name = StringField('Book Name', validators=[DataRequired()])
    book_author = StringField('Book Author', validators=[DataRequired()])
    book_rating = StringField('Book Rating', validators=[DataRequired()])
    submit = SubmitField('Submit')

    ##CREATE TABLE


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # def __repr__(self):
    #     return '<User %r>' % self.title


db.create_all()


@app.route('/delete/<book_id>')
def delete(book_id):
    print(book_id)
    delete_record(book_id)
    return redirect(url_for('home'))


@app.route('/edit', methods=['POST', 'GET'])
def edit():
    form = editForm()
    print(request.method)
    print(request.args.get('book_id'))
    edit_book = Book.query.filter_by(id=request.args.get('book_id')).first()

    if request.method == 'POST':
        print(request.form['bookid'])
        print(request.form['new_rating'])
        edit_book = Book.query.filter_by(id=int(request.form['bookid'])).first()
        edit_book.rating = float(request.form['new_rating'])
        db.session.commit()
        return redirect(url_for('home'))
    # print(edit_book.rating)
    # render_template("edit.html", book_id=book_id, form=editForm)

    return render_template("edit.html", form=form, book=edit_book)


def delete_record(_id):
    delete_book = Book.query.filter_by(id=_id).first()
    db.session.delete(delete_book)
    db.session.commit()


# INSERT RECORD
def insert_record(_title_, _author, _rating):
    new_book = Book(title=_title_, author=_author, rating=_rating)
    db.session.add(new_book)
    db.session.commit()


@app.route('/')
def home():
    # update = Book.query.filter_by(title="Harry Potter").first()
    # update.title = "Manny Rules"
    # db.session.commit()
    all_books = []
    for book in Book.query.all():
        print(book.title)

        book_dict = {
            "id": book.id,
            "title": book.title,
            "author": book.author,
            "rating": book.rating,
        }
        all_books.append(book_dict)

    return render_template("index.html", all_books=all_books)
    # return render_template("index.html", all_books=all_books)


@app.route("/add", methods=['POST', 'GET'])
def add():
    form = addBookForm()
    if form.validate_on_submit():
        insert_record(request.form['book_name'], request.form['book_author'], float(request.form['book_rating']))
        return redirect(url_for('home'))
    return render_template("add.html", form=form)


if __name__ == "__main__":
    app.run(debug=True, port=8081)
