import dash
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output, callback
import psycopg2 as pg
import pandas.io.sql as psql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

dash.register_page(__name__, path='/SONAR_Comparison')


#def connection(name):
 #   conn = pg.connect(
  #      host='gdash-d-usw2-databricks-rds.cbb8bn0jehcb.us-west-2.rds.amazonaws.com',
   #     database='databricksdb',
    #    user='cds_sonarrep_svc',
     ##   password='Giehwi38@)nbkfM'
    #)
    #dataframe = psql.read_sql('SELECT * FROM cds_metrics.sonar_dashboard_' + name, conn)
    #return dataframe






dash.register_page(__name__, path='/SONAR_Comparison')

layout = html.Div([
    html.H3("Comparison"),
    html.P("Data has not been loaded. Check your server console for the DataFrame output.")
])