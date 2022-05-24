from flask import *
import requests
import json
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():
    topic = 'buddhism'
    response = requests.get("http://gutendex.com/books/?topic="+topic)
    data = json.loads(response.content)
    books = data['results']
    
    author = 'nietzsche'
    response = requests.get("http://gutendex.com/books/?search="+author)
    data = json.loads(response.content)
    books2 = []
    books2 = data['results']
    
    sort = 'popular'
    response = requests.get("https://gutendex.com/books/?sort="+sort)
    data = json.loads(response.content)
    books3 = []
    books3 = data['results']    
        
    return render_template('/main/index.html', books=books, books2=books2, books3=books3)

@bp.route('/about')
def about():
    return render_template('/main/about.html')

