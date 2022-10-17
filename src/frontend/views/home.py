import pickle

from backend import Faculty
from config import config
from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__)

# get all objects
with open(config.SAVED_FILE, 'rb') as inp:
    s = pickle.load(inp)

db = Faculty()
db.extend(s)


@home_bp.route('/')
def homepage():
    '''
    creates a page to display all faculty members
    '''
    faculty_list = list(zip(db.faculty_list, db.links()))
    faculty_list = sorted(faculty_list, key=lambda x: x[0].name)
    return render_template('home.html', faculty_list=faculty_list)
