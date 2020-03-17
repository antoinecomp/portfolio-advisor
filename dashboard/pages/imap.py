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
data_path = 'data/maroc-swing.json'


def get_geojson():
    with open(join(base_dir, data_path), 'r') as fp:
        return json.load(fp)


def get_ids(geojson):
    return [feature.get('id') for feature in geojson['features']]


def get_z(geojson, view):
    zs = []
    for feature in geojson['features']:
        try:
            if view.isupper():
                z = feature['properties']['results'][view] / \
                    feature['properties']['voter_file']['nbre_inscrits']
            elif view == 'nbre_inscrits':
                z = feature['properties']['voter_file'][view]
            else:
                z = feature['properties'][view]
        except KeyError:
            z = 0
        zs.append(z)
    return zs


def get_hovertext(geojson):
    """
    return top 5 parties by number of polling stations won for each commune.
    """
    text = []
    for feat in geojson['features']:
        try:
            string = "<br>"
            commune = feat['properties']['name_4']
            results = feat['properties']['results']
            results_sorted = {k: v for k, v in sorted(results.items(),
                                                      key=lambda item: item[1],
                                                      reverse=True)}
            top = list(results_sorted.items())[:3]
            string += '<b>' + commune.upper() + '</b><br><br>'
            string += 'Top 3 Parties <br><br>'
            for i, t in enumerate(top):
                string += str(i+1) + ':  ' + t[0] + "   " + str(t[1]) + '<br>'
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
            zmin=np.percentile(get_z(geojson, view), 2),
            zmax=np.percentile(get_z(geojson, view), 95),
            colorscale='Reds',
            text=get_hovertext(geojson),
            hoverinfo='z+text',
            marker_opacity=0.4
        ),
        go.Layout(
            mapbox_style='carto-positron',
            mapbox_zoom=5.6,
            mapbox_center={'lat': 32, 'lon': -7},
            hovermode='closest',
            margin={'r': 0, 't': 0, 'l': 0, 'b': 0}
        )
    )


geojson = get_geojson()
ids = get_ids(geojson)
z = get_z(geojson, 'swing')


def layout():
    return html.Div([
        html.Div([
            html.H5('Select Type of View', style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='select-view',
                options=[
                    {'label': 'SWING - Total Swing Polling Stations',
                     'value': 'swing_count'},
                    {'label': 'SWING - Weighted by Total Polling Stations \
                         per Commune',
                     'value': 'swing_ratio'},
                    {'label': 'RESULTS - Turnout',
                     'value': 'turnout'},
                    {'label': 'RESULTS - Number of Registered Voters',
                     'value': 'nbre_inscrits'},
                    {'label': 'RESULTS - RNI',
                     'value': 'RNI'},
                    {'label': 'RESULTS - PJD',
                     'value': 'PJD'},
                    {'label': 'RESULTS - PAM',
                     'value': 'PAM'},
                    {'label': 'RESULTS - PI',
                     'value': 'PI'}
                ],
                value='swing_count'
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
                figure=get_map('swing_count'),
                style={
                    'width': 'auto',
                    'height': '750px',
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
    return get_map(view)
