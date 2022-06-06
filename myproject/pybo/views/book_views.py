from flask import *
import requests
import json
from pybo.form import UserCreateForm, UserLoginForm
from pybo.models import User
from pybo.models import Bookshelf

from .. import db

bp = Blueprint('book', __name__, url_prefix='/')

@bp.route('/details/')
def details():
    
    title = 'dickens%20great'
    response = requests.get("http://gutendex.com/books/?search="+title)
    data = json.loads(response.content)
    books = []
    books = data['results']
    
    author = 'nietzsche'
    response = requests.get("http://gutendex.com/books/?search="+author)
    data = json.loads(response.content)
    books2 = []
    books2 = data['results']   
        
    return render_template('book/details.html', books=books, books2=books2)

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
    
    return render_template('book/bookshelves.html')

@bp.route("/addToCart")
def addToCart():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    else:
        productId = int(request.args.get('productId'))
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId FROM users WHERE email = '" + session['email'] + "'")
            userId = cur.fetchone()[0]
            try:
                cur.execute("INSERT INTO kart (userId, productId) VALUES (?, ?)", (userId, productId))
                conn.commit()
                msg = "Added successfully"
            except:
                conn.rollback()
                msg = "Error occured"
        conn.close()
        return redirect(url_for('root'))