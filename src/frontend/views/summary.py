import json
import pickle

from backend import Faculty
from config import config
from flask import Blueprint, render_template, request, jsonify
from frontend.views.processes import Bar, Network, Scatter

summary_bp = Blueprint('summary_bp', __name__, url_prefix='/summary')

# get all objects
with open(config.SAVED_FILE, 'rb') as inp:
    s = pickle.load(inp)

db = Faculty()
db.extend(s)


@summary_bp.route("/")
def stats():
    '''
    summary page for stats containing:
    1. 2 Bars (total cites over years, count of interests)
    2. 1 Network (who worked with who on what reserach paper? NTU only)
    3. 2 Scatter (citations per publications, quality of paper vs grants)
    '''
    Bar(db).plot(page="summary",
                 filename=config.TOT_FCITES_PATH,
                 title="Cites per year",
                 xaxis_title="Year",
                 yaxis_title="No. of citations")
    Bar(db).plot(page="summary",
                 filename=config.TOT_FINTERESTS_PATH,
                 type="interests",
                 title="Interests",
                 xaxis_title="Count",
                 yaxis_title="Type",
                 height=2000)
    # remove non NTU coauthors
    db.filter_authors()
    Network(db).plot(filename=config.NET_PATH, edge_dict=None,
                     **config.NETWORK_CONFIG)
    Scatter(db).plot(filename=config.SCATTER_PATH_TOTAL,
                     title_text="Lifetime citations of every faculty against publications",
                     xaxis_title="Number of publications",
                     yaxis_title="Lifetime citations earned",
                     x=db.publications,
                     y=db.citations,
                     text=db.faculty,
                     marker=dict(size=db.grants,
                                 sizemode='area',
                                 sizeref=2.*max(db.grants)/(40.**2),
                                 sizemin=10),
                     **config.SCATTER_CONFIG)
    Scatter(db).plot(filename=config.SCATTER_PATH_QUALITY,
                     title_text="Quality of paper against grants received",
                     xaxis_title="Number of grants",
                     yaxis_title="Quality of paper",
                     x=db.grants,
                     y=[i / j for i, j in zip(db.citations, db.publications)
                        if j != 0],
                     text=db.faculty,
                     **config.SCATTER_CONFIG)
    return render_template("summary.html", faculty_list=db)


@summary_bp.route("/recommend_me")
def recommend_me():
    '''
    recommends grants based on interest
    '''
    selected = request.values.get('interest_select')
    grants = db.recommend_grants(selected)
    return jsonify(grants)


@summary_bp.route("/total_cites")
def show_totalcites():
    '''
    renders total citations plot
    '''
    return render_template('summary_cites.html')


@summary_bp.route("/total_interests")
def show_totalinterests():
    '''
    renders total interests plot
    '''
    return render_template('summary_interests.html')


@summary_bp.route("/network")
def show_network():
    '''
    renders network
    '''
    return render_template('summary_network.html')


@summary_bp.route("/scatter_plot")
def show_scatter():
    '''
    renders bubble chart of citations per publications vs grants
    '''
    return render_template('summary_scatter.html')


@summary_bp.route("/scatter_plot_q")
def show_scatter_q():
    '''
    renders quality of papers scatter plot
    '''
    return render_template('summary_scatter_q.html')
