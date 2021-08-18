import datashader as ds
import plotly.express as px
import pandas as pd
import numpy as np

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

np.random.seed(1)
N = 10000000
df = pd.DataFrame(dict(x=np.random.randn(N),
                       y=np.random.randn(N)))

cvs = ds.Canvas(plot_width=850, plot_height=500)
agg = cvs.points(df, x='x', y='y')


fig = px.imshow(agg, origin='lower', labels={'color':'Log10(count)'})
fig.update_traces(hoverongaps=False)
fig.update_layout(coloraxis_colorbar=dict(title='Count', tickprefix='1.e'))

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='N : %d'%N),
    dcc.Interval(id='interval1', interval=1000, n_intervals=0),
    html.H1(id='label1', children=''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

import dash.dependencies
@app.callback(dash.dependencies.Output('label1', 'children'),
    [dash.dependencies.Input('interval1', 'n_intervals')])
def update_interval(n):
    return 'Intervals Passed: ' + str(n)


if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
