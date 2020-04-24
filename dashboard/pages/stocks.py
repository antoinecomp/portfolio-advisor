import dash
import dash_table
import os
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
from yahooquery import Ticker
import plotly.express as px
import requests
import yfinance as yf

from ..server import app

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DATA_PATH = os.path.join(PROJECT_ROOT, '../data/')
df = pd.read_csv(DATA_PATH + 'tickers_september_2017_red.csv')


def layout():
    return html.Div([
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),

            sort_action='custom',
            sort_mode='single',
            sort_by=[]
        ),
        dbc.Modal(
            [
                dbc.ModalHeader("Header"),
                dbc.ModalBody("This is the content of the modal"),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            size="xl",
            id="modal",
        )
    ])


@app.callback(
    Output('table', 'data'),
    [Input('table', "page_current"),
     Input('table', "page_size"),
     Input('table', 'sort_by')])
def update_table(page_current, page_size, sort_by):
    if len(sort_by):
        dff = df.sort_values(
            sort_by[0]['column_id'],
            ascending=sort_by[0]['direction'] == 'asc',
            inplace=False
        )
    else:
        # No sort is applied
        dff = df

    return dff.iloc[
        page_current*page_size:(page_current+ 1)*page_size
    ].to_dict('records')


@app.callback(Output('modal', 'children'),
              [Input('table', 'active_cell'),
               Input('close', 'n_clicks')],
              # [State('modal', 'is_open')]
              )
def set_content(active_cell, n_clicks):
    if active_cell is not None:
        row = df.iloc[[active_cell.get("row")]]
        name = row['Name']
        ticker = row['Ticker']

    return [
        dbc.ModalHeader(name),
        dbc.ModalBody(
            html.Div([
                html.Div([
                    html.H6('Sales', style={'textAlign': 'center', 'padding': 10}),
                    html.P(update_earnings(ticker), id="sales_stocks", style={'textAlign': 'center', 'padding': 10})
                ], className='pretty_container four columns'),
                html.Div([
                    html.H5('Current ratio', style={'textAlign': 'center', 'padding': 10}),
                    dcc.Graph(id="current_ratio_stocks"),
                ], className='pretty_container seven columns')
            ])),
       # dbc.ModalBody(
       #      html.Div([
       #          html.Div([
       #              html.H5('Dividends', style={'textAlign': 'center', 'padding': 10}),
       #              dcc.Graph(id="dividends_stocks")
       #          ], className='pretty_container twelve columns'),
       #      ])),
            # html.Div([
            #     html.Div([
            #         html.H5('Earnings growth/10 years', style={'textAlign': 'center', 'padding': 10}),
            #         html.P("Earnings growth/10 years: ", id="earnings_growth", style={'textAlign': 'center', 'padding': 10})
            #     ], className='pretty_container four columns'),
            #     html.Div([
            #         html.H5('Earnings', style={'textAlign': 'center', 'padding': 10}),
            #         dcc.Graph(id="earnings")
            #     ], className='pretty_container seven columns')
            # ]), className='pretty_container twelve columns'),
        dbc.ModalFooter(dbc.Button("Close", id="close"))
    ]

@app.callback(
    Output('dividends_stocks', 'figure'),
    [Input('table', 'value')])
def update_dividends(active_cell):
    df = pd.read_csv(DATA_PATH + 'tickers_september_2017_red.csv')
    row = df.iloc[[active_cell.get("row")]]
    ticker = row['Ticker'].values[0]
    stock = yf.Ticker(ticker)
    dividends = stock.dividends
    df = pd.DataFrame(dividends).reset_index()
    fig = px.line(df, x='Date', y='Dividends')
    return fig

@app.callback(
    Output('current_ratio_stocks', 'figure'),
    [Input('table', 'active_cell')])
def update_current_ratio(active_cell):
    df = pd.read_csv(DATA_PATH + 'tickers_september_2017_red.csv')
    row = df.iloc[[active_cell.get("row")]]
    ticker = row['Ticker'].values[0]
    ticker = Ticker(ticker)
    df = ticker.balance_sheet()
    df = df.reset_index(drop=True)
    cols = df.columns

    totalCurrentAssets = df["totalCurrentAssets"][0]
    totalCurrentLiabilities = df["totalCurrentLiabilities"][0]

    ratio = float(totalCurrentAssets) / float(totalCurrentLiabilities)

    if ratio > 2:
        financial_status = "Conservatively financed"
    elif ratio > 1:
        financial_status = "Be careful"
    else:
        financial_status = "indebted"

    data = dict(
        asset_and_liability=[financial_status, "totalCurrentAssets", "totalCurrentLiabilities"],
        parent=["", financial_status, financial_status],
        value=[ratio, totalCurrentAssets, totalCurrentLiabilities]

    )

    fig = px.sunburst(
        data,
        names='asset_and_liability',
        parents='parent',
        values='value'
    )

    return fig


def update_earnings(ticker):
    # print("ticker: ", type(ticker))
    # print("ticker: ", ticker.values[0])
    ticker = Ticker(ticker.values[0])
    try:
        earnings = ticker.income_statement().totalRevenue[0]
        return earnings
    except Exception as e:
        print(e)


@app.callback(Output('modal', 'is_open'),
              [Input('table', 'active_cell'),
               Input('close', 'n_clicks')],
              [State("modal", "is_open")])
def toggle_modal(n1, n2, is_open):
    # print("n1: ", n1, " n2: ", n2)
    if n1 or n2:
        return not is_open
    return is_open

# @app.callback(
#     Output('earnings_growth', 'children'),
#     [Input('select-stock', 'value')])
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



if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
