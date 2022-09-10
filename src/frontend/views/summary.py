import logging
from backend import db, Faculty
from flask import Blueprint, render_template
import plotly.offline as py
from config import config

import networkx as nx
from pyvis.network import Network

import datetime
import plotly.graph_objects as go

summary_bp = Blueprint('summary_bp', __name__, url_prefix='/summary')

year = datetime.datetime.today().year


@summary_bp.route("/")
def stats():
    # total cites
    years = list(range(year, year - 30))
    total_cites = {k: 0 for k in years}
    for f in db.faculty_list:
        cpy = f.citesperyear
        total_cites.update({
            k: total_cites.get(k, 0) + cpy.get(k, 0)
            for k in set(total_cites) | set(cpy)
                          })
    # plot
    if all(i == 0 for i in list(total_cites.values())):
        logging.error("Dictionary cannot be updated")
    else:
        plot_cites(total_cites)
    # network
    # 1. remove co author if not in faculty
    # 2. create n^2 graph or relations (edges)
    # steps referred from:
    # https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259
    db.filter_authors()
    plot_network(db)
    return render_template("summary.html")


@summary_bp.route("/total_cites")
def show_totalcites():
    return render_template('summary_cites.html')


@summary_bp.route("/network")
def show_network():
    return render_template('summary_network.html')


def plot_cites(total_cites: dict):
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=list(total_cites.keys()),
               y=list(total_cites.values()))
                 )
    fig.update_layout(
        title="Cites per year",
        xaxis_title="Year",
        yaxis_title="No. of citations",)
    # TODO sort the dictionary keys in ascensding order
    py.plot(fig, filename=config.TOT_FCITES_PATH, auto_open=False)


def create_edge(db):
    edge_list_ = []
    for member in db.faculty_list:
        for coauthor in member.coauthors:
            edge_list_.append(tuple(sorted([member.name, coauthor])))
    edge_list = {i: edge_list_.count(i) for i in edge_list_}
    return edge_list


def plot_network(db: Faculty):
    G = nx.Graph()
    edge_list = create_edge(db)

    for member in db.faculty_list:
        G.add_node(member.name, data=member)

    for edge in edge_list:
        G.add_edge(*edge, weight=edge_list[edge])

    net = Network(notebook=True)
    net.from_nx(G)
    net.show(config.NET_PATH)
