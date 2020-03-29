from os.path import abspath, dirname, join

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output

import pandas as pd

import plotly.express as px
import numpy as np

from ..server import app

base_dir = dirname(dirname(abspath(__file__)))
data_path = 'data/tickers_september_2017.xlsx'


def get_tickers():
    with open(join(base_dir, data_path), 'rb') as fp:
        stock_df = pd.read_excel(fp)
        stock_df = stock_df.dropna()
        # stock_df = stock_df.where(pd.notnull(stock_df), None)
        return stock_df


df = get_tickers()


def layout():
    return html.Div([
        html.Div([
            html.Div([
                html.H5('Stocks', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id='graph',
                   figure=px.treemap(df, path=['Country', 'Exchange'], # values='pop',
                  # color='lifeExp', hover_data=['iso_alpha'],
                  # color_continuous_scale='RdBu',
                  # color_continuous_midpoint=np.average(df['lifeExp'], weights=df['pop'])
                ))
            ], className='pretty_container twelve columns'),
        ], className='pretty_container twelve columns')
    ])


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)