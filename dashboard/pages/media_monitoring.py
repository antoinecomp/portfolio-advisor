from os.path import abspath, dirname

import dash_core_components as dcc
import dash_html_components as html

import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Input, Output

import pandas as pd

from datetime import datetime as dt
from datetime import date

from collections import Counter

import requests
import json

import yfinance as yf

from itertools import chain

from . import utils
from ..server import app

@app.callback(
    Output('earnings', 'figure'),
    [Input('select-stock', 'value')])
def update_earnings(entity):
    pass

@app.callback(
    Output('current_ratio', 'figure'),
    [Input('select-stock', 'value')])
def update_current_ratio(entity):
    bs = requests.get(f'https://financialmodelingprep.com/api/v3/financials/balance-sheet-statement/AAPL?period=quarter')
    bs = bs.json()

    total_assets = bs.get("financials")[0].get("Total assets")

    # Assets
    cash_and_cash_equivalents = bs.get("financials")[0].get('Cash and cash equivalents')
    short_term_investments = bs.get("financials")[0].get('Short-term investments')
    cash_and_short_term_investments = bs.get("financials")[0].get('Cash and short-term investments')
    receivables = bs.get("financials")[0].get('Receivables')
    inventories = bs.get("financials")[0].get('Inventories')
    current_assets = [cash_and_cash_equivalents, short_term_investments, cash_and_short_term_investments, receivables,
                      inventories]

    property_plant_equipment_net = bs.get("financials")[0].get('Property, Plant & Equipment Net')
    goodwill_and_intangible_assets = bs.get("financials")[0].get('Goodwill and Intangible Assets')
    long_term_investments = bs.get("financials")[0].get('Long-term investments')
    tax_assets = bs.get("financials")[0].get('Tax assets')

    total_current_assets = bs.get("financials")[0].get('Total current assets')
    total_non_current_assets = bs.get("financials")[0].get('Total non-current assets')

    # liabilities
    payables = bs.get("financials")[0].get('Payables')
    short_term_debt = bs.get("financials")[0].get('Short-term debt')
    total_current_liabilities = bs.get("financials")[0].get('Total current liabilities')

    long_term_debt = bs.get("financials")[0].get('Long-term debt')
    # total_debt = bs.get("financials")[0].get('Total debt')
    deferred_revenue = bs.get("financials")[0].get('Deferred revenue')
    tax_liabilities = bs.get("financials")[0].get('Tax Liabilities')
    deposit_liabilities = bs.get("financials")[0].get('Deposit Liabilities')
    total_non_current_liabilities = bs.get("financials")[0].get("Total non-current liabilities")

    total_liabilities = bs.get("financials")[0].get('Total liabilities')

    ratio = float(total_assets)/float(total_liabilities)

    if ratio > 2:
        financial_status = "Conservatively financed"
    elif ratio > 1:
        financial_status = "Be careful"
    else:
        financial_status = "indebted"

    data = dict(
        asset_and_liability =[financial_status, "total_assets", "total_liabilities", "total_current_assets",
                              "Cash_and_cash_equivalents", "Short_term_investments", "Cash_and_short_term_investments",
                              "Receivables", "Inventories", "total_non_current_assets", "property_plant_equipment_net",
                              "goodwill_and_intangible_assets", "long_term_investments", "tax_assets",
                              "total_current_liabilities", "total_non_current_liabilities"],
        parent=["", financial_status, financial_status, "total_assets", "total_current_assets",
                "total_current_assets", "total_current_assets", "total_current_assets", "total_current_assets",
                "total_assets", "total_non_current_assets", "total_non_current_assets", "total_non_current_assets",
                "total_non_current_assets", "total_liabilities", "total_liabilities"],
        value=[ratio, total_assets, total_liabilities, total_current_assets, cash_and_cash_equivalents,
               short_term_investments, cash_and_short_term_investments, receivables, inventories,
               total_non_current_assets, property_plant_equipment_net, goodwill_and_intangible_assets,
               long_term_investments, tax_assets, total_current_liabilities, total_non_current_liabilities])

    fig = px.sunburst(
        data,
        names='asset_and_liability',
        parents='parent',
        values='value',
    )

    return fig

@app.callback(
    Output('dividends', 'figure'),
    [Input('select-stock', 'value')])
def update_current_ratio(entity):
    stock = yf.Ticker(entity)
    dividends = stock.dividends
    df = pd.DataFrame(dividends).reset_index()
    fig = px.line(df, x='Date', y='Dividends')
    return fig

from ..server import app

""" Test entities """
stock1 = {"label": "Microsoft", "value": "msft"}

STOCK_LIST = [stock1]

base_dir = dirname(dirname(abspath(__file__)))

server = app.server


def layout():
    return html.Div([
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='select-stock',
                    options=STOCK_LIST,
                    value=STOCK_LIST[0].get('value')
                )
            ])
        ], className='pretty_container twelve columns'),
        html.Div([
            html.Div([
                html.H5('Sales', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="sales")
            ], className='pretty_container four columns'),
            html.Div([
                html.H5('Current ratio', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="current_ratio")
            ], className='pretty_container seven columns')
        ]),
        html.Div([
            html.Div([
                html.H5('Dividends', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="dividends")
            ], className='pretty_container twelve columns'),
        ]),
        html.Div([
            html.Div([
                html.H5('Earnings growth/10 years', style={'textAlign': 'center', 'padding': 10}),
                # dcc.Graph(id="sales")
            ], className='pretty_container four columns'),
            html.Div([
                html.H5('Earnings', style={'textAlign': 'center', 'padding': 10}),
                # dcc.Graph(id="current_ratio")
            ], className='pretty_container seven columns')
        ]),
    ], className='pretty_container twelve columns')


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)
