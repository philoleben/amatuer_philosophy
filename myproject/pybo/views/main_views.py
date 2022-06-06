from flask import *
import requests
import json
from werkzeug.utils import redirect
from pybo.models import Question
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():

    books = []
    model = Doc2Vec.load("C:\\gu.model")
    f = open('C:\\키없는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    
    def recommend_title(text):
        # a = requests.get(json_data[text]['full-text']).text
        new_vector = model.infer_vector(word_tokenize(text))
        sims = model.dv.most_similar([new_vector])
        return sims

    def recommend_full_text(text):
        for t in json_data:
            if t['title'] == text:
                full_text = requests.get(t['full-text']).text
                break;
        
        new_vector = model.infer_vector(word_tokenize(full_text))
        sims = model.dv.most_similar([new_vector])
        return sims
    
    for book in json_data:
        if book['authors'] == 'Plato':
            books.append(book)
        books2 = []
    
    a = sorted(json_data, key = lambda x: x['download_count'], reverse=True)
    
    for i in range(10):
        books2.append(a[i])
    
    books3 = []
    
    lists = recommend_full_text('The Philosophy of Spinoza')
    lists.pop(0)
    for book in json_data:
        for t in lists:
            if book['title'] == t[0]:
                books3.append(book)
        
    return render_template('/main/index.html', books=books, books2=books2, books3=books3)

@bp.route('/about')
def about():
    return render_template('/main/about.html')

