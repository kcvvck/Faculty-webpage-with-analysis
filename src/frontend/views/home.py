from backend.load import db
from flask import Blueprint, render_template

home_bp = Blueprint('home_bp', __name__)


@home_bp.route('/')
def homepage():
    faculty_list = list(zip(db.faculty_list, db.links()))
    return render_template('home.html', faculty_list=faculty_list)