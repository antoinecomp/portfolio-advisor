from flask import Flask
from dash import Dash
#import dash_auth

VALID_CREDENTIALS = {
    'UserAux': 'AppyAux5GS'
}

server = Flask('dashboard')

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
#auth = dash_auth.BasicAuth(app, VALID_CREDENTIALS)

app.config['suppress_callback_exceptions'] = True
