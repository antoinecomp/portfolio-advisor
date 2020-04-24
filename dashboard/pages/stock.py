from os.path import abspath, dirname
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import requests
import yfinance as yf
from yahooquery import Ticker


from ..server import app

@app.callback(
    Output('sales', 'children'),
    [Input('select-stock', 'value')])
def update_earnings(entity):
    ticker = entity
    url = 'https://financialmodelingprep.com/'
    api = 'api/v3/financials/income-statement/'
    search_api_url = url + api + ticker
    response = requests.get(
        search_api_url
    )
    json = response.json()
    earnings = json['financials'][0]['Revenue']
    earnings = float(earnings)
    return '{:,.2f}'.format(earnings)


@app.callback(
    Output('current_ratio', 'figure'),
    [Input('select-stock', 'value')])
def update_current_ratio(entity):
    ticker = Ticker(entity)
    df = ticker.balance_sheet()
    df = df.reset_index(drop=True)
    cols = df.columns

    # I need to get rid of it if doesn't exists
    # Assets
    cash = df["cash"][0]
    shortTermInvestments = df["shortTermInvestments"][0]
    netReceivables = df["netReceivables"][0]
    inventory = df["inventory"][0]
    otherCurrentAssets = df["otherCurrentAssets"][0]
    totalCurrentAssets = df["totalCurrentAssets"][0]
    longTermInvestments = df["longTermInvestments"][0]
    propertyPlantEquipment = df["propertyPlantEquipment"][0]
    goodWill = df["goodWill"][0]
    intangibleAssets = df["intangibleAssets"][0]
    otherAssets = df["otherAssets"][0]
    deferredLongTermAssetCharges = df["deferredLongTermAssetCharges"][0]
    totalAssets = df["totalAssets"][0]

    # liabilities
    accountsPayable = df["accountsPayable"][0]
    otherCurrentLiab = df["otherCurrentLiab"][0]
    longTermDebt = df["longTermDebt"][0]
    otherLiab = df["otherLiab"][0]
    totalCurrentLiabilities = df["totalCurrentLiabilities"][0]
    totalLiab = df["totalLiab"][0]
    commonStock = df["commonStock"][0]
    retainedEarnings = df["retainedEarnings"][0]
    treasuryStock = df["treasuryStock"][0]
    otherStockholderEquity = df["otherStockholderEquity"][0]
    totalStockholderEquity = df["totalStockholderEquity"][0]
    netTangibleAssets = df["netTangibleAssets"][0]

    ratio = float(totalCurrentAssets) / float(totalCurrentLiabilities)

    if ratio > 2:
        financial_status = "Conservatively financed"
    elif ratio > 1:
        financial_status = "Be careful"
    else:
        financial_status = "indebted"

    data = dict(
        asset_and_liability=[financial_status, totalCurrentAssets, "totalCurrentLiabilities"],
        parent=["", financial_status, financial_status],
        value=[ratio, totalCurrentAssets, totalCurrentLiabilities]

    )

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
def update_dividends(entity):
    stock = yf.Ticker(entity)
    dividends = stock.dividends
    df = pd.DataFrame(dividends).reset_index()
    fig = px.line(df, x='Date', y='Dividends')
    return fig

@app.callback(
    Output('earnings', 'figure'),
    [Input('select-stock', 'value')])
def update_earnings(entity):
    ticker = entity
    url = 'https://financialmodelingprep.com/'
    api = 'api/v3/financials/income-statement/'
    search_api_url = url + api + ticker
    response = requests.get(
        search_api_url
    )
    json = response.json()
    earnings = json['financials']
    df = pd.DataFrame(earnings)[['date', 'Revenue']]
    fig = px.line(df, x='date', y='Revenue')
    return fig

@app.callback(
    Output('earnings_growth', 'children'),
    [Input('select-stock', 'value')])
def update_earnings_growth(entity):
    ticker = entity
    url = 'https://financialmodelingprep.com/'
    api = 'api/v3/financials/income-statement/'
    search_api_url = url + api + ticker
    response = requests.get(
        search_api_url
    )
    json = response.json()
    earnings = json['financials']
    df = pd.DataFrame(earnings)['Revenue']
    pct_change = pd.to_numeric(df).pct_change(-1)
    mean_growth = pct_change.mean(skipna = True)
    return '{:.2%}'.format(mean_growth)


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
                html.H6('Sales', style={'textAlign': 'center', 'padding': 10}),
                html.P("Sales: ", id="sales", style={'textAlign': 'center', 'padding': 10})
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
                html.P("Earnings growth/10 years: ", id="earnings_growth", style={'textAlign': 'center', 'padding': 10})
            ], className='pretty_container four columns'),
            html.Div([
                html.H5('Earnings', style={'textAlign': 'center', 'padding': 10}),
                dcc.Graph(id="earnings")
            ], className='pretty_container seven columns')
        ]),
    ], className='pretty_container twelve columns')


if __name__ == "__main__":
    app.run_server(debug=False, port=8051)
