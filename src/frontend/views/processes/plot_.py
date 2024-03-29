import datetime
import logging
import operator
from collections import OrderedDict
from dataclasses import dataclass
from typing import Dict

import networkx as nx
import plotly.graph_objects as go
import plotly.offline as py
from backend import Faculty
from backend.facultymember import FacultyMember
from config import config

year = datetime.datetime.today().year
years = list(range(year, year - 30))


@dataclass
class Plot:
    '''
    Parent class: ensures all plot objects have plot method
    '''
    db: Faculty

    def plot(self, filename: str = None, **kwargs):
        if not filename:
            return None


@dataclass
class Bar(Plot):
    '''
    configurations for bar plots
    '''
    def _cpreload(self) -> Dict[int, int]:
        """
        citations graph in the form
        {
            "year1": "citation1",
            ...
        }
        """
        total_cites = {k: 0 for k in years}
        for f in self.db.faculty_list:
            cpy = f.citesperyear
            total_cites.update({
                k: total_cites.get(k, 0) + cpy.get(k, 0)
                for k in set(total_cites) | set(cpy)
                            })
        total_cites = OrderedDict(sorted(total_cites.items()))
        if all(i == 0 for i in list(total_cites.values())):
            logging.error("Dictionary of cites cannot be updated")
        else:
            return total_cites

    def _ipreload(self) -> Dict[str, int]:
        """
        interests graph in the form
        {
            "interest": count
        }
        """
        total_interest = self.db.unique_interest()
        total_interest = dict(
            {i: len(total_interest[i]) for i in total_interest.keys()}
            )
        updated = {k: v for k, v in total_interest.items() if v > 1}
        return updated

    def plot(self, page: str = None,
             faculty: FacultyMember = None,
             filename: str = None,
             type: str = "cites",
             **kwargs):
        '''
        Plot bar plots for different pages as
        they have different configurations
        '''
        if page == 'summary':
            if type == "interests":
                data = self._ipreload()
            else:
                data = self._cpreload()
        elif page == 'profile':
            data = faculty.citesperyear
        else:
            return None
        fig = go.Figure()
        # get key of max value for highlighting bar
        max_key = max(data.items(), key=operator.itemgetter(1))[0]
        # interest bar configurations
        if type == "interests":
            data = dict(sorted(data.items(), key=operator.itemgetter(1)))
            max_list = [config.DEFAULT_COL if i != max_key
                        else config.MAX_COLOR for i in data.keys()]
            fig.add_trace(
                go.Bar(x=list(data.values()),
                       y=list(data.keys()),
                       orientation="h",
                       text=list(data.values()),
                       textposition="outside",
                       marker=dict(color=max_list))
                        )
        # citations bar configurations
        else:
            max_list = [config.DEFAULT_COL if i != max_key
                        else config.MAX_COLOR for i in data.keys()]
            fig.add_trace(
                go.Bar(x=list(data.keys()),
                       y=list(data.values()),
                       marker=dict(color=max_list))
                        )
        fig.update_layout(**kwargs)
        py.plot(fig, filename=filename, auto_open=False)


@dataclass
# Network referred from:
# https://towardsdatascience.com/visualizing-networks-in-python-d70f4cbeb259
# https://www.kaggle.com/code/anand0427/network-graph-with-at-t-data-using-plotly/notebook
class Network(Plot):
    def plot(self, filename: str = None,
             edge_dict: Dict[str, str] = None,
             **kwargs):
        '''
        Plot Network graph
        '''
        xtextpos = []
        ytextpos = []
        edgepos = []
        G = nx.Graph()
        if not edge_dict:
            edge_dict = self.create_edge()
        # add nodes and edges
        for member in self.db.faculty_list:
            G.add_node(member.name, data=member)
        for edge in edge_dict:
            G.add_edge(*edge, weight=edge_dict[edge])
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
            same_pub = self.db.set_pub(edge[0], edge[1])
            # Found that some coauthors, even though are listed,
            # do not have the same publications
            # on their google scholar
            edgepos.append(('<br>'.join(same_pub) if same_pub
                            else "No information"))
        # add interactive weight trace
        # edgetext = str(edgepos)[2:-2].replace(', ', '<br>')
        eweights_trace = go.Scatter(x=xtextpos, y=ytextpos,
                                    text=edgepos,
                                    **config.WEIGHT_CONFIG)
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
        return edge_dict


@dataclass
class Scatter(Plot):
    def plot(self, filename: str = None,
             title_text: str = None,
             xaxis_title: str = None,
             yaxis_title: str = None,
             **kwargs):
        '''
        Plot scatter plots for different pages as
        they have different configurations
        '''
        fig = go.Figure()
        fig.add_trace(go.Scatter(**kwargs))
        if title_text == "Lifetime citations of every faculty against publications":
            shapes = []
            colors = ["#f0f9e8", "#bae4bc", "#7bccc4", "#2b8cbe"]
            start_coord = [(0.5, 0), (0, 0), (0.5, 0.5), (0, 0.5)]
            end_coord = [(1, 0.5), (0.5, 0.5), (1, 1), (0.5, 1)]
            for idx, i in enumerate(colors):
                shapes.append(dict(type="rect",
                                   xref="paper",
                                   yref="paper",
                                   x0=start_coord[idx][0],
                                   y0=start_coord[idx][1],
                                   x1=end_coord[idx][0],
                                   y1=end_coord[idx][1],
                                   fillcolor=i,
                                   opacity=0.5,
                                   layer="below",
                                   line_width=0
                                   ))
            fig.update_layout(title_text=title_text,
                              xaxis_title=xaxis_title,
                              yaxis_title=yaxis_title,
                              width=800,
                              shapes=shapes)
            fig.update_xaxes(showgrid=False)
            fig.update_yaxes(showgrid=False)
        else:
            fig.update_layout(title_text=title_text,
                              xaxis_title=xaxis_title,
                              yaxis_title=yaxis_title,
                              width=800)

        fig.write_html(filename)
