from pybo import db

class User(db.Model): 
    __tablename__ = 'user'   #테이블 이름 : user
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    username = db.Column(db.String(8), nullable = False)
    email = db.Column(db.String(32), nullable = False)     
    password = db.Column(db.String(64), nullable = False) 
    subjects = db.Column(db.String(64))
    authors = db.Column(db.String(8))
    
class Categories(db.Model): 
    __tablename__ = 'categories'   #테이블 이름 : bookshelf
    id = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    name = db.Column(db.Text())

# 좋아요 기능을 위한 table     
class Book(db.Model):
    __tablename__ = 'book'   #테이블 이름 : user
    id = db.Column(db.Integer, primary_key=True)
    bookid = db.Column(db.Integer, nullable=False)
    voter = db.relationship('User', secondary='book_voter', backref=db.backref('book_voter_set'))


class Bookshelf(db.Model): 
    __tablename__ = 'bookshelf'   #테이블 이름 : bookshelf
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    bookid = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))
    
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('question_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref=db.backref('answer_set', cascade='all, delete-orphan'))
    content = db.Column(db.Text(), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))
    
book_voter = db.Table(
    'book_voter',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), primary_key=True),
    db.Column('book_id', db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'), primary_key=True)
)
