from flask import *
import requests
import json
from werkzeug.utils import redirect
from pybo.models import Question, Book, book_voter
from gensim.models.doc2vec import Doc2Vec
from nltk.tokenize import word_tokenize
import random
from pybo import db

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():

    # quote 중복 여부 확인
    def check(seq):
        seen = []
        unique_list = [x for x in seq if x not in seen and not seen.append(x)]
        return len(seq) == len(unique_list)
    
    temp = []
    books_for_authors = []
    
    model = Doc2Vec.load("C:\\gu.model")
    
    f = open('C:\\키없는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    
    q = open('quote.json', 'r', encoding= "UTF-8")
    quote = json.load(q, strict=False)
    
    # f2 = open('C:\\키 있는거.json', 'r', encoding="UTF-8")
    # json_data2 = json.load(f2, strict=False)
    
    # book_id 값을 db에 저장
    # for book in json_data:   

    #     data = Book(bookid=book['id']+1)
    #     db.session.add(data)
    #     db.session.commit()
    
    # book_id 값을 db에 삭제
    # db.session.query(Book).delete()
    # db.session.commit()
    
    def recommend_title(text):
        new_vector = model.infer_vector(word_tokenize(text))
        sims = model.dv.most_similar([new_vector])
        return sims

    def recommend_full_text(text):
        sims = model.dv.most_similar(model.dv[text])
        return sims
    
    vote_data = []
    for book in json_data:
        if book['authors'] == 'Plato':
            data = Book.query.filter_by(bookid=book['id']).first()
            book["voter"] = len(data.voter)
            books_for_authors.append(book)
    # print(books_for_authors)
        
    books2 = []
    a = sorted(json_data, key = lambda x: x['download_count'], reverse=True)
    
    for i in range(10):
        books2.append(a[i])
    
    books3 = []
    
    lists = recommend_full_text('Aristotle on the art of poetry')
    lists.pop(0)

    # 키 없는거 사용 
    for book in json_data:
        for t in lists:
            if book['title'] == t[0]:
                books3.append(book)
    
    """
    키 있는거 
    for book in lists:
        books3.append(json_data2[book])
    
    """
    # print(json.dumps(books_for_authors, indent="\t") )
    
    quote_list = []
    idx = []
    
    for i in range(5):
        idx.append([random.randint(0, 11), 0])
    
    quote_json = quote['results']
    while True:
        for i in range(5):
            idx[i][1] = random.randint(0, len(quote_json[ idx[i][0] ]['ideas']) - 1)

        if check(idx):
            break;
    
    
    for i in range(5):
        quote_list.append([quote_json[idx[i][0]]['name'], quote_json[idx[i][0]]['photo'], quote_json[idx[i][0]]['ideas'][idx[i][1]]])
    
    return render_template('/main/index.html', books=books_for_authors, books2=books2, books3=books3, quote_list=quote_list)

@bp.route('/about')
def about():
    return render_template('/main/about.html')

