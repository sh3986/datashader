import datashader as ds
import pandas as pd
import numpy as np

np.random.seed(1)
N = 100000
df = pd.DataFrame(dict(x=np.random.randn(N),
                       y=np.random.randn(N)))

cvs = ds.Canvas(plot_width=850, plot_height=500)
agg = cvs.points(df, x='x', y='y')

# # agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
# coords_lat, coords_lon = agg.coords['Lat'].values, agg.coords['Lon'].values
# # Corners of the image, which need to be passed to mapbox
# coordinates = [[coords_lon[0], coords_lat[0]],
#                 [coords_lon[-1], coords_lat[0]],
#                 [coords_lon[-1], coords_lat[-1]],
#                 [coords_lon[0], coords_lat[-1]]]

from colorcet import fire
import datashader.transfer_functions as tf
img = tf.shade(agg, cmap='darkblue')[::-1].to_pil()

import plotly.express as px
# Trick to create rapidly a figure with mapbox axes
fig = px.scatter_mapbox(df[:1],  lat='x', lon='y')
# Add the datashader image as a mapbox layer image
fig.update_layout(mapbox_style="carto-darkmatter",
                mapbox_layers = [
                {
                    "sourcetype": "image",
                    "source": img
                }]
)

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8080)
