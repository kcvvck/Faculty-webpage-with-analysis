import plotly.offline as py
# import plotly.plotly as py

import plotly.express as px
import plotly.graph_objects as go
from backend.load import db

f = db.faculty_list
member = f[0]
fig = go.Figure()
fig.add_trace(go.Bar(x=list(member.citesperyear.keys()), y=list(member.citesperyear.values())))
fig.update_layout(
    title="Cites per year",
    xaxis_title="Year",
    yaxis_title="No. of citations",)

py.plot(fig, filename='citesperyear.html', auto_open=False)
# print(url)
# fig.show()

# first_plot_url = py.plot(data, filename='cites per year', auto_open=False,)
# print(first_plot_url)