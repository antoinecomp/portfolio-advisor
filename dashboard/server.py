from flask import Flask
from dash import Dash
#import dash_auth
import dash_bootstrap_components as dbc


VALID_CREDENTIALS = {
    'UserAux': 'AppyAux5GS'
}

server = Flask('dashboard')

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
#auth = dash_auth.BasicAuth(app, VALID_CREDENTIALS)

app.config['suppress_callback_exceptions'] = True
