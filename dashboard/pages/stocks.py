import dash
import dash_table
import os
import pandas as pd
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_bootstrap_components as dbc

from ..server import app

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

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


@app.callback(Output('ModalHeader', 'children'),
              [Input('table', 'active_cell'),
              Input('close', 'n_clicks')],
              # [State('modal', 'is_open')]
              )
def update_graph(active_cell, n_clicks):
    print("active_cell: ", active_cell)
    if active_cell is not None:
        row = df.iloc[[active_cell.get("row")]]
        # return dbc.Modal(
        #     [
        #         dbc.ModalHeader(row['Name'].values[0]),
        #         dbc.ModalBody("This will be something more interesting"),
        #         dbc.ModalFooter(
        #             dbc.Button("Close", id="close", className="ml-auto")
        #         ),
        #     ],
        #     id="modal",
        # )
        return row['Name'].values[0]


@app.callback(Output('modal', 'is_open'),
              [Input('table', 'active_cell'),
               Input('close', 'n_clicks')],
              [State("modal", "is_open")])
def toggle_modal(n1, n2, is_open):
    # print("n1: ", n1, " n2: ", n2)
    if n1 or n2:
        return not is_open
    return is_open





if __name__ == '__main__':
    app.run_server(debug=False, port=8051)
