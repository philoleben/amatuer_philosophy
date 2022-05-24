from pybo import db

class User(db.Model): 
    __tablename__ = 'user'   #테이블 이름 : user
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    username = db.Column(db.String(8), nullable = False)
    email = db.Column(db.String(32), nullable = False)     
    password = db.Column(db.String(64), nullable = False) 
    author = db.Column(db.String(8))
    genre = db.Column(db.String(64))
    audio = db.Column(db.Integer)
    