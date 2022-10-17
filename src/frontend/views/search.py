import pickle

from backend import Faculty
from config import config
from flask import Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

search_bp = Blueprint('search_bp', __name__, url_prefix='/search')

# get all objects
with open(config.SAVED_FILE, 'rb') as inp:
    s = pickle.load(inp)

db = Faculty()
db.extend(s)

# can be
# 2018, 2022/ >1000
# 2013- 2017/ 900-4000
# 2013- 2017/ 900, 4000
# 2014/ <10
# 2014/ 400
CHOICES = [('Interests', 'Interests'),
           ('Grants', 'Grants'),
           ('Publications', 'Publications'),
           ('Citations', 'Citations - <year-range>/<citation-range>')]


class SearchForm(FlaskForm):
    """
    Search bar
    """
    select = SelectField(
        'Select query',
        choices=CHOICES
    )

    search = StringField(
        'Query',
        [DataRequired()]
    )
    submit = SubmitField("Search")


@search_bp.route('/', methods=("GET", "POST"))  # name has + for whitespace
# code referenced from: https://www.tutorialspoint.com/flask/flask_wtf.htm
def search():
    '''
    Search page
    '''
    form = SearchForm()
    if request.method == 'POST':
        if form.validate() is False:
            return render_template('404.html')
        else:
            selected = form.select.data
            query = form.search.data
            fc = db.find_all(selected, query)
            return render_template('search.html', form=form, fc=fc)
    elif request.method == 'GET':
        return render_template('search.html', form=form, fc=[])
