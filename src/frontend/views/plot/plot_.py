import datetime
import logging
from collections import OrderedDict
from dataclasses import dataclass

import networkx as nx
import plotly.graph_objects as go
import plotly.offline as py
from backend import Faculty
from config import config

year = datetime.datetime.today().year
years = list(range(year, year - 30))


@dataclass
class Plot:
    db: Faculty

    def plot(self, filename=None, **kwargs):
        if not filename:
            return None


@dataclass
class Bar(Plot):
    def _spreload(self):
        total_cites = {k: 0 for k in years}
        for f in self.db.faculty_list:
            cpy = f.citesperyear
            total_cites.update({
                k: total_cites.get(k, 0) + cpy.get(k, 0)
                for k in set(total_cites) | set(cpy)
                            })
        total_cites = OrderedDict(sorted(total_cites.items()))
        if all(i == 0 for i in list(total_cites.values())):
            logging.error("Dictionary cannot be updated")
        else:
            return total_cites

    def plot(self, page=None, faculty=None, filename=None, **kwargs):
        if page == 'summary':
            data = self._spreload()
        elif page == 'profile':
            data = faculty.citesperyear
        else:
            return None
        fig = go.Figure()
        fig.add_trace(
            go.Bar(x=list(data.keys()),
                   y=list(data.values()))
                    )
        fig.update_layout(**kwargs)
        py.plot(fig, filename=filename, auto_open=False)


@dataclass
class Network(Plot):
    def plot(self, filename=None, edge_list=None, **kwargs):
        xtextpos = []
        ytextpos = []
        edgepos = []
        G = nx.Graph()
        if not edge_list:
            edge_list = self.create_edge()
        # add nodes and edges
        for member in self.db.faculty_list:
            G.add_node(member.name, data=member)
        for edge in edge_list:
            G.add_edge(*edge, weight=edge_list[edge])
        # referred from:
        # https://www.kaggle.com/code/anand0427/network-graph-with-at-t-data-using-plotly/notebook
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        for n, p in pos.items():
            G.nodes[n]['pos'] = p
        # add edge and node trace (interactive traces)
        edge_trace = go.Scatter(**config.EDGE_CONFIG)
        node_trace = go.Scatter(**config.NODE_CONFIG)
        for edge in G.edges():
            x0, y0 = G.nodes[edge[0]]['pos']
            x1, y1 = G.nodes[edge[1]]['pos']
            edge_trace['x'] += tuple([x0, x1, None])
            edge_trace['y'] += tuple([y0, y1, None])
            xtextpos.append((x0+x1)/2)
            ytextpos.append((y0+y1)/2)
            edgepos.append(self.db.set_pub(edge[0], edge[1]))
        # add interactive weight trace
        eweights_trace = go.Scatter(x=xtextpos, y=ytextpos,
                                    text=edgepos, **config.WEIGHT_CONFIG)
        # add attributes to nodes
        for node in G.nodes():
            x, y = G.nodes[node]['pos']
            node_trace['x'] += tuple([x])
            node_trace['y'] += tuple([y])
        for node, adjacencies in enumerate(G.adjacency()):
            node_trace['marker']['color'] += tuple([len(adjacencies[1])])
            node_info = adjacencies[0] + ' # of connections: ' + \
                str(len(adjacencies[1]))
            node_trace['text'] += tuple([node_info])
        # plot
        fig = go.Figure(data=[edge_trace, node_trace, eweights_trace],
                        layout=go.Layout(**kwargs))
        fig.write_html(filename)

    def create_edge(self):
        edge_list_ = []
        for member in self.db.faculty_list:
            for coauthor in member.coauthors:
                # create edge list [['member1', 'member2'],...]
                edge_list_.append(tuple(sorted([member.name, coauthor])))
        # count weights
        edge_dict = {i: edge_list_.count(i) for i in edge_list_}
        # get similar publications
        edge_list_ = set(edge_list_)
        # similarpubs = {i: db.set_pub(i[0], i[1]) for i in edge_list_}
        return edge_dict  # , similarpubs


@dataclass
class Scatter(Plot):
    def plot(self, filename=None, **kwargs):
        fig = go.Figure()
        fig.add_trace(go.Scatter(**kwargs))
        fig.write_html(filename)
