from flask import Blueprint, render_template
from pybo.models import Question
bp = Blueprint('question', __name__, url_prefix='/question')

@bp.route('/board/')
def board():
    # 조회한 데이터를 create_date값 기준으로 역순으로 정렬
    question_list = Question.query.order_by(Question.create_date.desc())
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    # get_or_404 함수는 해당 데이터를 찾을 수 없는 경우 404페이지를 출력
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question)