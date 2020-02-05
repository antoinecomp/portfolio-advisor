import json

import dash_daq as daq
import plotly.graph_objects as go
import dash_core_components as dcc
import dash_html_components as html

from .server import app, server
from .pages import header, imap, sources

mapbox_access_token = ("pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtM"
                       "zNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w")


app.layout = html.Div(
    [
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),

        # Header
        header.layout(),

        dcc.Tabs(
            [
                dcc.Tab(
                    label='Electoral Map',
                    value='electoral',
                    children=imap.layout()
                ),
                dcc.Tab(
                    label='Media Monitoring',
                    value='media-monitoring'
                ),
                dcc.Tab(
                    label='Research Map',
                    value='research',
                    children=sources.layout()
                )
              #  dcc.Tab(
              #      label='Search article',
              #      value='search'
              #  )
            ]
        )
    ]
)
