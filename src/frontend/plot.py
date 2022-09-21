
def plot_cites(db):
    years = list(range(year, year - 30))
    total_cites = {k: 0 for k in years}
    for f in db.faculty_list:
        cpy = f.citesperyear
        total_cites.update({
            k: total_cites.get(k, 0) + cpy.get(k, 0)
            for k in set(total_cites) | set(cpy)
                          })
    total_cites = OrderedDict(sorted(total_cites.items()))
    if all(i == 0 for i in list(total_cites.values())):
        logging.error("Dictionary cannot be updated")
    else:
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
            # create edge list [['member1', 'member2'],...]
            edge_list_.append(tuple(sorted([member.name, coauthor])))
    # count weights
    edge_dict = {i: edge_list_.count(i) for i in edge_list_}
    # get similar publications
    edge_list_ = set(edge_list_)
    # similarpubs = {i: db.set_pub(i[0], i[1]) for i in edge_list_}
    return edge_dict  # , similarpubs


def plot_network(db: Faculty):
    xtextpos = []
    ytextpos = []
    edgepos = []
    G = nx.Graph()
    edge_list = create_edge(db)

    for member in db.faculty_list:
        G.add_node(member.name, data=member)

    for edge in edge_list:
        G.add_edge(*edge, weight=edge_list[edge])

    # referred from:
    # https://www.kaggle.com/code/anand0427/network-graph-with-at-t-data-using-plotly/notebook
    pos = nx.spring_layout(G, k=0.5, iterations=50)
    for n, p in pos.items():
        G.nodes[n]['pos'] = p
    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines')

    for edge in G.edges():
        x0, y0 = G.nodes[edge[0]]['pos']
        x1, y1 = G.nodes[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
        xtextpos.append((x0+x1)/2)
        ytextpos.append((y0+y1)/2)
        edgepos.append(db.set_pub(edge[0], edge[1]))
    eweights_trace = go.Scatter(x=xtextpos, y=ytextpos, mode='markers',
                                marker_size=0.5,
                                text=edgepos,
                                textposition='top center',
                                hoverinfo='text')

    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            colorscale='Bluered',
            reversescale=True,
            color=[],
            size=15,
            colorbar=dict(
                thickness=10,
                title='Connection strength',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=0)))
    for node in G.nodes():
        x, y = G.nodes[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])
    for node, adjacencies in enumerate(G.adjacency()):
        node_trace['marker']['color'] += tuple([len(adjacencies[1])])
        node_info = adjacencies[0] + ' # of connections: ' + \
            str(len(adjacencies[1]))
        node_trace['text'] += tuple([node_info])
    fig = go.Figure(data=[edge_trace, node_trace, eweights_trace],
                    layout=go.Layout(
                    title='NTU SCSE Research Network',
                    titlefont=dict(size=16),
                    showlegend=False,
                    hovermode='closest',
                    margin=dict(b=20, l=5, r=5, t=40),
                    annotations=[dict(
                        text="No. of connections",
                        showarrow=False,
                        xref="paper", yref="paper")],
                    xaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False,
                               showticklabels=False)))
    fig.write_html(config.NET_PATH)


def plot_scatter(db: Faculty):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
                            x=db.publications,
                            y=db.citations,
                            mode='markers',
                            text=db.faculty,
                            marker=dict(
                                        size=db.grants,
                                        sizemode='area',
                                        sizeref=2.*max(db.grants)/(40.**2),
                                        sizemin=10,
                                    ),
                            hovertemplate='name: %{text}' +
                                          '<br>publications:%{x}' +
                                          '<br>citations:%{y}',
                    ))
    fig.write_html(config.SCATTER_PATH)
