from backend import db
from config import config
from flask import Blueprint, render_template

from frontend.views.plot import Bar, Network, Scatter

summary_bp = Blueprint('summary_bp', __name__, url_prefix='/summary')


@summary_bp.route("/")
def stats():
    # total cites
    # network
    # 1. remove co author if not in faculty
    # 2. create n^2 graph or relations (edges)
    # steps referred from:
    # https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259
    # plot
    Bar(db).plot(page="summary",
                 filename=config.TOT_FCITES_PATH,
                 title="Cites per year",
                 xaxis_title="Year",
                 yaxis_title="No. of citations")
    Bar(db).plot(page="summary",
                 filename=config.TOT_FINTERESTS_PATH,
                 type="interests",
                 title="Interests",
                 xaxis_title="Type",
                 yaxis_title="Count")
    db.filter_authors()
    Network(db).plot(filename=config.NET_PATH, edge_dict=None,
                     **config.NETWORK_CONFIG)
    Scatter(db).plot(filename=config.SCATTER_PATH,
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
    return render_template("summary.html")


@summary_bp.route("/total_cites")
def show_totalcites():
    return render_template('summary_cites.html')


@summary_bp.route("/total_interests")
def show_totalinterests():
    return render_template('summary_interests.html')


@summary_bp.route("/network")
def show_network():
    return render_template('summary_network.html')


@summary_bp.route("/scatter_plot")
def show_scatter():
    return render_template('summary_scatter.html')
