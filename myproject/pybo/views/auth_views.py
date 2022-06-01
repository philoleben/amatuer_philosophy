from flask import *
from pybo.form import UserCreateForm, UserLoginForm
from pybo.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

bp = Blueprint('auth', __name__, url_prefix='/')

@bp.route('/signup/', methods=['GET','POST'])
def signup():
    form = UserCreateForm()

    genre_data=[{'genre': 'Literature'}, {'genre': 'History'}, {'genre': 'Philosophy'}]
    author_data=[{'author': 'Spinoza'}, {'author': 'Karl Marx'}, {'author': 'Nietzsche'}]  
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data,
                        password=generate_password_hash(form.password1.data),
                        email=form.email.data,
                        genre = request.form.get('genre'),
                        author = request.form.get('author'),
                        audio = request.form.get('way')
                        )
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')
    return render_template('auth/signup.html', form=form, genre_data=genre_data, author_data=author_data)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            error = "존재하지 않는 사용자입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)


'''라우팅 함수보다 항상 먼저 실행'''
# 세션을 조사하여 로그인 여부 확인
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)
        
@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

@bp.route('/bookshelves/', methods=('GET', 'POST'))
def bookshelves():
    user_id = session.get('user_id')
    if user_id is None:
        return redirect(url_for('auth.login'))
    return render_template('auth/bookshelves.html')

