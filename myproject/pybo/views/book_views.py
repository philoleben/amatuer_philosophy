from flask import *
import requests
import json
from pybo.form import UserCreateForm, UserLoginForm
from pybo.models import User
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
