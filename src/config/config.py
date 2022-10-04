from pathlib import Path

TAG = "div"
CLASS = "img-card__body"
URL = ["https://dr.ntu.edu.sg/simple-search?query=&location=researcherprofiles&filter_field_1=school&filter_type_1=authority&filter_value_1=ou00030&crisID=&relationName=&sort_by=bi_sort_4_sort&order=asc&rpp=50&etal=0&start=0",
       "https://dr.ntu.edu.sg/simple-search?query=&location=researcherprofiles&filter_field_1=school&filter_type_1=authority&filter_value_1=ou00030&crisID=&relationName=&sort_by=bi_sort_4_sort&order=asc&rpp=50&etal=0&start=50"]
WEBSITE = "display-label-personalsite"
AKA = {"Jagath Chandana Rajapakse": "Jagath C. Rajapakse",
       "Ke Yiping, Kelly": "Yiping Ke",
       "Lana Obraztsova": "Svetlana Obraztsova"
       }
ROOT = str(Path().absolute())
DATA_FILE = ROOT + "/src/backend/data"
FCITES_PATH = ROOT + '/src/frontend/templates/citesperyear.html'
TOT_FCITES_PATH = ROOT + '/src/frontend/templates/summary_cites.html'
TOT_FINTERESTS_PATH = ROOT + '/src/frontend/templates/summary_interests.html'
NET_PATH = ROOT + '/src/frontend/templates/summary_network.html'
SCATTER_PATH = ROOT + '/src/frontend/templates/summary_scatter.html'
EDGE_CONFIG = {'x': [], 'y': [],
               'line': dict(width=0.5, color='#888'),
               'hoverinfo': 'none', 'mode': 'lines'}
NODE_CONFIG = {'x': [],
               'y': [],
               'text': [],
               'mode': 'markers',
               'hoverinfo': 'text',
               'marker': dict(
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
                     line=dict(width=0))}
WEIGHT_CONFIG = {'mode': 'markers',
                 'marker_size': 0.5,
                 'textposition': 'top center',
                 'hoverinfo': 'text'}
NETWORK_CONFIG = {'title': 'NTU SCSE Research Network',
                  'titlefont': dict(size=16),
                  'showlegend': False,
                  'hovermode': 'closest',
                  'margin': dict(b=20, l=5, r=5, t=40),
                  'annotations': [dict(
                         text="No. of connections",
                         showarrow=False,
                         xref="paper", yref="paper")],
                  'xaxis': dict(showgrid=False, zeroline=False,
                                showticklabels=False),
                  'yaxis': dict(showgrid=False, zeroline=False,
                                showticklabels=False)}
SCATTER_CONFIG = {'mode': 'markers',
                  'hovertemplate': 'name: %{text}' +
                                   '<br>publications:%{x}' +
                                   '<br>citations:%{y}'
                  }
