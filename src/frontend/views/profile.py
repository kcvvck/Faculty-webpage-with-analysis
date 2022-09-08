from backend.facultymember import FacultyMember
from backend.load import db
from flask import Blueprint, render_template
import plotly.offline as py
from config import config

import plotly.graph_objects as go

profile_bp = Blueprint('profile_bp', __name__, url_prefix='/profile')


@profile_bp.route('/<name>')  # name has + for whitespace
def profile(name):
    rname = name.replace("+", " ")
    f = db.get_member(rname)
    plot_cites(f)
    if not f:
        return render_template("404.html")
    return render_template("profile.html", faculty=f)


@profile_bp.route('/citesperyear')
def show_citeframe():
    return render_template('citesperyear.html')


def plot_cites(faculty: FacultyMember):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=list(faculty.citesperyear.keys()),
               y=list(faculty.citesperyear.values()))
                 )
    fig.update_layout(
        title="Cites per year",
        xaxis_title="Year",
        yaxis_title="No. of citations",)

    py.plot(fig, filename=config.FCITES_GRAPH, auto_open=False)
