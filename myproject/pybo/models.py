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
    
class Categories(db.Model): 
    __tablename__ = 'categories'   #테이블 이름 : bookshelf
    categoryid = db.Column(db.Integer, primary_key = True)   #id를 프라이머리키로 설정
    name = db.Column(db.Text())
        
class Book(db.Model):
    __tablename__ = 'book'   #테이블 이름 : user
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text())
    image = db.Column(db.Text())
    categoryid = db.Column(db.Integer, db.ForeignKey('categories.categoryid', ondelete='CASCADE'))
            

class Bookshelf(db.Model): 
    __tablename__ = 'bookshelf'   #테이블 이름 : bookshelf
    bookshlefid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    bookid = db.Column(db.Integer, db.ForeignKey('book.id', ondelete='CASCADE'))