import dash
import pandas as pd
from dash import Dash, dcc, html, Input, Output, callback, dash_table
import psycopg2 as pg
import pandas.io.sql as psql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

dash.register_page(__name__, path='/SONAR_Help')

layout = html.Div([
    html.H3("Help"),
    html.P("Data has not been loaded. Check your server console for the DataFrame output.")
])