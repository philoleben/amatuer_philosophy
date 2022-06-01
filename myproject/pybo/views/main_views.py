from flask import *
import requests
import json
from werkzeug.utils import redirect
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/')
def index():

    books = []
    f = open('C:\\book.json', 'r', encoding='UTF-8')
    json_data = json.load(f, strict=False)
    print(json.dumps(json_data, indent="\t"))
        
    return render_template('/main/index.html', books=books)

@bp.route('/about')
def about():
    return render_template('/main/about.html')

