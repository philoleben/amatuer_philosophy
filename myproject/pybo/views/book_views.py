from flask import *
import requests
import json
from pybo.form import UserCreateForm, UserLoginForm
from pybo.models import User
from pybo.models import Bookshelf, Book
from pybo.views.auth_views import login_required
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

from .. import db

bp = Blueprint('book', __name__, url_prefix='/')

f = open('키없는거.json', 'r', encoding='UTF-8')
json_data = json.load(f, strict=False)

@bp.route('/details/')
def details():
    book_id = int(request.args.get('bookId'))
    book = json_data[book_id]
    print(book_id)
    
    desc_list = book['description']

    author = book['authors']
    print(author)
    this_authors_otherbooks = []
    for _book in json_data:
        if _book['authors'] == author:
            this_authors_otherbooks.append(_book)
            
    # same subjects or Doc2vec ?        
        
    return render_template('book/details.html', book=book, this_authors_otherbooks=this_authors_otherbooks, desc_list=desc_list)

@bp.route('/search/')
def search():
    model = Doc2Vec.load("gu.model")
    f = open('키있는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    
    def recommend_title(text):
        new_vector = model.infer_vector(word_tokenize(text))
        sims = model.dv.most_similar([new_vector])
        return sims

    books = []
    temp = []
    if 'book' in request.args:
        search_word = request.args.get('book')
        
        lists = recommend_title(search_word)
        
        for idx in lists:
            temp.append(idx[0])

        for idx in range(len(temp)):
            books.append(json_data[temp[idx]])
        
    return render_template('book/results.html', books=books)

@bp.route('/bookshelves/', methods=('GET', 'POST'))
def bookshelves():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    
    book_data = Bookshelf.query.filter_by(userid=user_id).all() #현재 로그인한 user가 저장한 책 리스트 
    books = []
    for book in book_data:
        if book.bookid == None:
            continue
        else:
            books.append(json_data[book.bookid])
            
    return render_template('book/bookshelves.html', books=books)

@bp.route("/addToBookshelves")
@login_required
def addToBookshelves():

    user_id = session.get('user_id')
    book_id = request.args.get('bookId', type = int)
    book = Bookshelf.query.filter_by(userid=user_id,bookid=book_id).first() # 이미 저장된 데이터인지 확인
    if not book:
        bookshelf = Bookshelf(userid=user_id,bookid=book_id)
        db.session.add(bookshelf)
        db.session.commit()
        flash('Added Successfully.')   
    else:
        flash('Already Added.')    

    if(request.args.get('page')=='details'):
        url='/details?bookId='+str(book_id)
        return redirect(url)        
    else:
        return redirect(url_for('main.index'))
    
    
@bp.route("/delete/<int:bookshelf_id>")
def delete(bookshelf_id):
    
    book = Bookshelf.query.get(bookshelf_id)
    print(book)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for('book.bookshelves'))

@bp.route('/vote/<int:book_id>/')
@login_required
def vote(book_id):
    _book = Book.query.get_or_404(book_id)  
    _book.voter.append(g.user)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/ebook/<int:book_id>')
def ebook(book_id):
    
    f = open('키없는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    book_url = json_data[book_id]['full-text']
    print(book_url)
    return redirect(book_url)