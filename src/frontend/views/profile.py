from backend import db
from config import config
from flask import Blueprint, render_template
from frontend.views.processes import Bar

profile_bp = Blueprint('profile_bp', __name__, url_prefix='/profile')
page = "profile"


@profile_bp.route('/<name>')  # name has + for whitespace
def profile(name):
    '''
    creates a single profile page
    '''
    rname = name.replace("+", " ")
    f = db.get_member(rname)
    if f is None:
        return render_template("404.html")
    Bar(db).plot(page=page, faculty=f,
                 filename=config.FCITES_PATH,
                 xaxis_title="Year",
                 yaxis_title="No. of citations")
    return render_template("profile.html", faculty=f)


@profile_bp.route('/citesperyear')
def show_citeframe():
    '''
    render plotly saved html interactive graph
    in webpage
    '''
    return render_template('citesperyear.html')
