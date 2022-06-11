from flask import *
import requests
import json
from pybo.form import UserCreateForm, UserLoginForm
from pybo.models import User
from pybo.models import Bookshelf
from pybo.views.auth_views import login_required

from .. import db

bp = Blueprint('book', __name__, url_prefix='/')

@bp.route('/details/<int:book_id>')
def details(book_id):
    
    f = open('C:\\키없는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    book = json_data[book_id]
        
    return render_template('book/details.html',  book=book)

@bp.route('/search/')
def search():
    books = []
    if 'book' in request.args:
        search_word = request.args.get('book')
        response = requests.get("http://gutendex.com/books/?search="+search_word)
        data = json.loads(response.content)
        books = data['results']
    return render_template('book/results.html', books=books)

@bp.route('/bookshelves/', methods=('GET', 'POST'))
def bookshelves():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    
    books = []
    books = Bookshelf.query.filter_by(userid=user_id).all() #현재 로그인한 user가 저장한 책 리스트
    print(books)
    
    return render_template('book/bookshelves.html', books=books)

@bp.route("/addToBookshelves/<int:book_id>")
@login_required
def addToBookshelves(book_id):

    print(book_id)
    user_id = session.get('user_id')
    book = Bookshelf.query.filter_by(userid=user_id,bookid=book_id).first()
    if not book:
        bookshelf = Bookshelf(userid=user_id,bookid=book_id)
        db.session.add(bookshelf)
        db.session.commit()
        flash('Added Successfully.')   
    else:
        flash('Already Added.')    
        
        
    return redirect(url_for('main.index'))

@bp.route("/delete/int:<bookshelf_id>")
def delete(bookshelf_id):
    
    book = Bookshelf.query.get(bookshelf_id)
    print(book)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.bookshelves'))