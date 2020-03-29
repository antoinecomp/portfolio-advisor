import json
import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from .server import app #, auth, server
from .pages import header, imap, media_monitoring, stocks

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
                    label='Geography',
                    value='Geography',
                    children=imap.layout()
                ),
                dcc.Tab(
                    label='Stock',
                    value='Stock',
                    children=media_monitoring.layout()
                ),
                dcc.Tab(
                    label='Stocks',
                    value='Stocks',
                    children=stocks.layout()
                )
            ]
        )
    ]
)

if __name__ == "__main__":
    app.run_server(debug=False, port=8051)


