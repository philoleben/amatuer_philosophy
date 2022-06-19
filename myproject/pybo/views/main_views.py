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
    
    # 랜덤 저자 추출
    def get_random_authors():
        while True:
           idx = random.randint(0, len(json_data) - 1)
           author = json_data[idx]['authors'] 
           count = 0
           for title in json_data:
               if title['authors'] == author:
                   count += 1
            
           if count >= 3:
               break;       
        return author 

    # 랜덤 subject 추출
    def get_random_subjects():
        while True:
           idx = random.randint(0, len(json_data) - 1)
           select_subject = json_data[idx]['subjects'][random.randint(0, len(json_data[idx]['subjects']) - 1)]
           
           subject_list = []
           count = 0
           for sub_list in json_data:
                if select_subject in sub_list['subjects']:
                    count += 1
            
           if count >= 3:
               break;  
        
        
        return select_subject
    
    # 입력받은 데이터를 기반으로 검색하는 기능
    def recommend_title(text):
        new_vector = model.infer_vector(word_tokenize(text))
        sims = model.dv.most_similar([new_vector])
        return sims

    # 책 제목을 기반으로 유사도 측정
    def recommend_full_text(text):
        sims = model.dv.most_similar(model.dv[text])
        return sims
    
#-------------------------- json 파일 및 데이터 load ---------------------    

    model = Doc2Vec.load("C:\\gu.model")
    
    f = open('C:\\키없는거.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    
    q = open('quote.json', 'r', encoding= "UTF-8")
    quote = json.load(q, strict=False)
      
    # book_id 값을 db에 저장
    # for book in json_data:   

    #     data = Book(bookid=book['id']+1)
    #     db.session.add(data)
    #     db.session.commit()
    
    # book_id 값을 db에 삭제
    # db.session.query(Book).delete()
    # db.session.commit()
    
#---------------------------작가 랜덤으로 선택 후 데이터 가져오기-------------------------- 
    
    temp = []
    books_for_authors = []
    
    vote_data = []
    author = get_random_authors()
    
    for book in json_data:
        if book['authors'] == author:
            data = Book.query.filter_by(bookid=book['id']).first()
            book["voter"] = len(data.voter)
            books_for_authors.append(book)
    
    # print(books_for_authors)
        
#-----------------------------------download count 내림차순 정렬-----------------------------------------------    
    
    books2 = []
    download_desc = sorted(json_data, key = lambda x: x['download_count'], reverse=True)
    
    for idx in range(10):
        data = Book.query.filter_by(bookid=download_desc[idx]['id']).first()
        json_data[download_desc[idx]['id']]['voter'] = len(data.voter)
        books2.append(json_data[download_desc[idx]['id']])

#-----------------------------------------랜덤 subject --------------------------------------

    subject1 = get_random_subjects()
    subject2 = get_random_subjects()
    while subject1 == subject2:
        subject2 = get_random_subjects()
    
    books3 = [subject1]
    for book in json_data:
        if subject1 in book['subjects']:
            data = Book.query.filter_by(bookid=book['id']).first()
            book["voter"] = len(data.voter)
            books3.append(book)
    
    books4 = [subject2]
    for book in json_data:
        if subject2 in book['subjects']:
            data = Book.query.filter_by(bookid=book['id']).first()
            book["voter"] = len(data.voter)
            books4.append(book)
            
#--------------------------------------------------------------------------------------------------
    lists = recommend_full_text('Aristotle on the art of poetry')
    lists.pop(0)

    # 키 없는거 사용 

    

    # print(json.dumps(books_for_authors, indent="\t") )
    
#----------------------------------------인용구 추출 ------------------------------------------------
  
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

#--------------------------------------------------전달---------------------------------------------------------- 
    
    return render_template('/main/index.html', books=books_for_authors, author=books_for_authors[0]['authors'], books2=books2,  books3 = books3, books4 = books4, quote_list=quote_list)

#---------------------------------------------------------------------------------------------------------------------
@bp.route('/about')
def about():
    return render_template('/main/about.html')

