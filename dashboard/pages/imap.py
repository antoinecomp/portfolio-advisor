import json
import random
from os.path import abspath, dirname, join

import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

base_dir = dirname(dirname(abspath(__file__)))
data_path = 'data/maroc-swing.json'


def get_data():
    with open(join(base_dir, data_path), 'r') as fp:
        return json.load(fp)


def get_ids(geojson):
    return [feature.get('id') for feature in geojson['features']]


def get_z(geojson):
    z = []
    for feature in geojson['features']:
        try:
            swing = feature['properties']['swing_count']
        except KeyError:
            swing = 0
        z.append(swing)
    return z


def get_hovertext(geojson):
    """
    return top 5 parties by number of polling stations won for each commune.
    """
    pass


geojson = get_data()
ids = get_ids(geojson)
z = get_z(geojson)


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
                        z=z,  # [random.random() for i in range(len(ids))],
                        zmin=0,
                        zmax=40,
                        colorscale='Reds',
                        marker_opacity=0.4
                    ),
                    go.Layout(
                        mapbox_style='carto-positron',
                        mapbox_zoom=5.75,
                        mapbox_center={'lat': 32, 'lon': -7},
                        hovermode='closest',
                        margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
                    )
                ),
                style={
                    'width': 'auto',
                    'height': '800px',
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


def callback():
    pass
