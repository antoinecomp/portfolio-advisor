import json
import random
from os.path import abspath, dirname, join

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

base_dir = dirname(dirname(abspath(__file__)))
data_path = 'data/maroc.json'

with open(join(base_dir, data_path), 'r') as fp:
    geojson = json.load(fp)

ids = [feature.get('id') for feature in geojson['features']]


def layout():
    return html.Div([
        html.Div([
            html.H5('features', style={'textAlign': 'center'}),
            dcc.RadioItems(
                id='select-view',
                options=[
                    {'label': 'label', 'value': 'value'}
                ],
                value='value',
                labelStyle={'display': 'inline-block'}
            )
        ], style={
            'float': 'center',
            'display': 'inline-block',
            'text-align': 'center'
        }, className='bare_container twelve columns'
        ),
        html.Div([
            dcc.Graph(
                id='imap',
                figure=go.Figure(
                    go.Choroplethmapbox(
                        geojson=geojson,
                        locations=ids,
                        z=[random.random() for i in range(len(ids))],
                        colorscale='Reds',
                        marker_opacity=0.5
                    ),
                    go.Layout(
                        mapbox_style='carto-positron',
                        mapbox_zoom=5,
                        mapbox_center={'lat': -7, 'lon': 33},
                        hovermode='closest',
                        margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
                    )
                ),
                style={
                    'width': 'auto',
                    'height': 'auto',
                    'display': 'block',
                    'margin-left': 'auto',
                    'margin-right': 'auto',
                    'margin-top': '100px'
                }
            )
        ], style={'align-items': 'center'}
        )
    ], className='pretty_container twelve columns'
    )
