import dash_html_components as html

from ..server import app


def image(file, identification, style=None):
    return html.Img(
        src=app.get_asset_url(file),
        id=identification,
        style={
            "height": '65px',
            "width": 'auto',
            "margin-bottom": "30px",
        }
    )


def layout():
    return html.Div([
        html.Div(
            [image('auspex.png', 'auspex-logo')],
            style={'textAlign': 'left'},
            className="one-third column"
        ),
        html.Div([
            html.Div([
                html.H1(
                    "RNI Dashboard",
                    style={"margin-bottom": "10px"},
                )
            ], style={'text-align': 'center'}
            )
        ], className="one-half column", id="title",
        ),
        html.Div(
            [image('rni_logo.png', 'lelo-logo')],
            style={'text-align': 'right'},
            className="one-third column",
        )
    ], id="header",
       className="row flex-display",
       style={"margin-bottom": "30px"},
    )
