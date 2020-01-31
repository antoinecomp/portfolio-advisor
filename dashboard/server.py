from flask import Flask
from dash import Dash

server = Flask('dashboard')

app = Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.config['suppress_callback_exceptions'] = True
