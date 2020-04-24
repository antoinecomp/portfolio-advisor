import json
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from dashboard.server import app #, auth, server
from dashboard.pages import header, imap, stock, markets, stocks

mapbox_access_token = ("pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtM"
                       "zNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w")

server = app.server

app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),

        # Header
        header.layout(),

        dcc.Tabs(
            [
                dcc.Tab(
                    label='Best defensive stocks',
                    value='Stocks',
                    children=stocks.layout()
                ),
                dcc.Tab(
                    label='Search a stock',
                    value='Stock',
                    children=stock.layout()
                ),
                dcc.Tab(
                    label='Markets worldwide',
                    value='Markets',
                    children=markets.layout()
                ),
                # dcc.Tab(
                #     label='Geography',
                #     value='Geography',
                #     children=imap.layout()
                # )
            ]
        )
    ]
)



if __name__ == "__main__":
    app.run_server(debug=False, port=8051)


