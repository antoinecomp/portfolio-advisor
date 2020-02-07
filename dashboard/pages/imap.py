import json
import random
from os.path import abspath, dirname, join

import numpy as np
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from ..server import app

base_dir = dirname(dirname(abspath(__file__)))
data_path = 'data/maroc-swing-2.json'


def get_geojson():
    with open(join(base_dir, data_path), 'r') as fp:
        return json.load(fp)


def get_ids(geojson):
    return [feature.get('id') for feature in geojson['features']]


def get_z(geojson, weighted=False):
    z = []
    for feature in geojson['features']:
        try:
            swing = feature['properties']['swing_count']
            stations = feature['properties']['polling_station_count']
        except KeyError:
            swing = 0
        if weighted:
            z.append((swing / stations))
        else:
            z.append(swing)
    return z


def get_hovertext(geojson):
    """
    return top 5 parties by number of polling stations won for each commune.
    """
    text = []
    for feat in geojson['features']:
        try:
            string = ""
            results = feat['properties']['results']
            results_sorted = {k: v for k, v in sorted(results.items(),
                                                    key=lambda item: item[1],
                                                    reverse=True)}
            top = list(results_sorted)[:3]
            for t in top:
                string += t + '<br>'
            text.append(string)
        except KeyError:
            text.append('NO DATA')
    return text


def get_map(view):
    return go.Figure(
        go.Choroplethmapbox(
            geojson=get_geojson(),
            locations=get_ids(geojson),
            z=get_z(geojson, view),
            zmin=0,
            zmax=np.percentile(get_z(geojson, view), 95),
            colorscale='Reds',
            hovertext=get_hovertext(geojson),
            marker_opacity=0.4
        ),
        go.Layout(
            mapbox_style='carto-positron',
            mapbox_zoom=5.75,
            mapbox_center={'lat': 32, 'lon': -7},
            hovermode='closest',
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
    )


geojson = get_geojson()
ids = get_ids(geojson)
z = get_z(geojson)


def layout():
    return html.Div([
        html.Div([
            html.H5('features', style={'textAlign': 'center'}),
            dcc.RadioItems(
                id='select-view',
                options=[
                    {'label': 'swing', 'value': 'swing'},
                    {'label': 'swing weighted', 'value': 'swing-weighted'}
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
                figure=get_map(True),
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


@app.callback(
    Output('imap', 'figure'),
    [Input('select-view', 'value')]
)
def callback(view):
    if view == 'swing-weighted':
        return get_map(True)
    else:
        return get_map(False)
