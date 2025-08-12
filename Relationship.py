import dash
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
#from scipy import stats
import psycopg2 as pg
import pandas.io.sql as psql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

dash.register_page(__name__, path='/SONAR_Relationship')

layout = html.Div([
    html.H3("Relationship"),
    html.P("Data has not been loaded. Check your server console for the DataFrame output.")
])