import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import psycopg2 as pg
import pandas.io.sql as psql
from sqlalchemy import create_engine
import pandas as pd
import urllib.parse

def connection(name):
 #   conn = pg.connect(
  #      host='gdash-d-usw2-databricks-rds.cbb8bn0jehcb.us-west-2.rds.amazonaws.com',
     #   database='databricksdb',
   #     user='cds_sonarrep_svc',
    #    password='Giehwi38@)nbkfM'
    #)
    #dataframe = psql.read_sql('SELECT * FROM cds_metrics.sonar_dashboard_' + name, conn)
    #return dataframe
    host='gdash-d-usw2-databricks-rds.cbb8bn0jehcb.us-west-2.rds.amazonaws.com',
    database='databricksdb',
    user='cds_sonarrep_svc',
    password='Giehwi38@)nbkfM'
    
    password = urllib.parse.quote_plus("Giehwi38@)nbkfM")
    #print(password)

    #engine = create_engine('postgresql://cds_sonarrep_svc:password@gdash-d-usw2-databricks-rds.cbb8bn0jehcb.us-west-2.rds.amazonaws.com:5432/databricksdb')

    #dataframe = psql.read_sql(f'SELECT * FROM cds_metrics.sonar_dashboard_{name}', engine)
    engine = create_engine(f"postgresql://cds_sonarrep_svc:{password}@gdash-d-usw2-databricks-rds.cbb8bn0jehcb.us-west-2.rds.amazonaws.com:5432/databricksdb")
    dataframe = pd.read_sql('SELECT * FROM cds_metrics.sonar_dashboard_' + name, engine)
    #dataframe = psql.read_sql('SELECT * FROM cds_metrics.sonar_dashboard_' + name, conn)
    #return dataframe

# PART 0: load in data source
source = 'aggregated'
#df_sonar = connection(source)
df_sonar_simplely = pd.read_csv("data/Aggregate_Dashboard.csv")
dash.register_page(__name__, path='/')

# PART I: Data Preprocessing:
# 1. Set working df to a copy of raw to prevent corruption of original data
# 2. Create new column StatusCount' from 'Study#'
# 3. Drop the 'Study#' column
# 4. Select only the needed columns from dataframe
#print (df_sonar_simple)
#df_sonar_simple = df_sonar
df_sonar_simple = df_sonar_simplely.copy()
df_sonar_simple['StatusCount'] = df_sonar_simple['Study#']
df_sonar_simple = df_sonar_simple.drop('Study#', axis=1)
df_sonar_simple = df_sonar_simple[['TA', 'Phase', 'Year', 'TotalStudies', 'StatusCount', 'Status', 'EDCBuilds', 'DBL',
                                   'FinalTFL', 'PROTtoEDC_Median', 'LPLVtoDBL_Median', 'DBLtoTFL_Median',
                                   'NumCRF_Median',
                                   'NumQueries_Median', 'NumTFLs_Median', 'NumMigrationLE2_perc', 'NumStudyDBUL_perc',
                                   'NumTFLsLE250_perc']]

#print (df_sonar_simple)
# Create the layout of the app
layout = html.Div(className='general_container',
                  # Main body of the dashboard. (Everything below the header)
                  # First layer is a general invisible container that formats the alignment of the other containers.
                  children=[
                      html.Div(className='body_container',
                               children=[
                                   # Left side of the dashboard. (Section that contains
                                   # This container arranges the elements in to a columns and aligns them in the center
                                   html.Div(className='left_column',
                                            # Container for the current year dropdown selector and its title
                                            children=[
                                                html.Div(style={'width': '175px',
                                                                'margin': '25px'},
                                                         # Container and title for the dropdown selector
                                                         children=[
                                                             html.Div('Select Year',
                                                                      style={'color': '#F0F0F0',
                                                                             'font-family': 'Arial',
                                                                             'margin': '3px'}),
                                                             # Dropdown selector for Current Year
                                                             # Displays a list of unique values in the 'Year' column of the dataframe
                                                             # Default value set to 2022
                                                             # Callback ID is 'current-year'
                                                             dcc.Dropdown(
                                                                 df_sonar_simple['Year'].unique(),
                                                                 id='current-year',
                                                                 value=2025,
                                                                 style={
                                                                     'font-family': 'Arial, sans-serif',
                                                                     'border-radius': '0px',
                                                                     'height': '20px',
                                                                     'background-color': '#F0F0F0'},
                                                                 clearable=False),
                                                         ]),
                                                # Container for the compared year dropdown selector and its title
                                                html.Div(style={'width': '175px',
                                                                'margin': '25px'},
                                                         # Container and title for the Compared Year selector
                                                         children=[
                                                             html.Div('Select Compared Year',
                                                                      style={'color': '#F0F0F0',
                                                                             'font-family': 'Arial',
                                                                             'margin': '3px'}),
                                                             # Dropdown selector for Compared Year
                                                             # Displays a list of unique values in the 'Year' column of the dataframe
                                                             # Default value set to 2022
                                                             # Callback ID is 'compared-year'
                                                             dcc.Dropdown(
                                                                 df_sonar_simple['Year'].unique(),
                                                                 id='compared-year',
                                                                 value=2024,
                                                                 style={
                                                                     'font-family': 'Arial, sans-serif',
                                                                     'border-radius': '0px',
                                                                     'height': '20px',
                                                                     'background-color': '#F0F0F0'},
                                                                 clearable=False),
                                                         ]),
                                                # Container for TA checklist selector and its title
                                                html.Div(style={'width': '175px',
                                                                'margin': '25px'},
                                                         children=[
                                                             html.Div('Select TA',
                                                                      style={'color': '#F0F0F0',
                                                                             'font-family': 'Arial',
                                                                             'margin': '3px'}),
                                                             dcc.Dropdown(
                                                                 df_sonar_simple['TA'].unique(),
                                                                 id='selected-TA',
                                                                 value='All',
                                                                 style={
                                                                     'font-family': 'Arial, sans-serif',
                                                                     'border-radius': '0px',
                                                                     'height': '20px',
                                                                     'background-color': '#F0F0F0'},
                                                                 clearable=False),
                                                         ]),
                                                html.Div(style={'width': '175px',
                                                                'margin': '25px'},
                                                         children=[
                                                             html.Div('Select Phase',
                                                                      style={'color': '#F0F0F0',
                                                                             'font-family': 'Arial',
                                                                             'margin': '3px'}),
                                                             dcc.Dropdown(
                                                                 df_sonar_simple['Phase'].unique(),
                                                                 id='selected-phase',
                                                                 value='All',
                                                                 style={
                                                                     'font-family': 'Arial, sans-serif',
                                                                     'border-radius': '0px',
                                                                     'height': '20px',
                                                                     'background-color': '#F0F0F0'},
                                                                 clearable=False),
                                                         ]),
                                                html.Div(className='legend_container',
                                                         children=[
                                                             html.Div(className='legend_item_container',
                                                                      children='Study Status'),
                                                             html.Div(className='legend_item_container',
                                                                      children=[
                                                                          html.Div(
                                                                              className='legend_icon_green'),
                                                                          'Completed']),
                                                             html.Div(className='legend_item_container',
                                                                      children=[
                                                                          html.Div(
                                                                              className='legend_icon_red'),
                                                                          'InitiatedStudies']),
                                                             html.Div(className='legend_item_container',
                                                                      children=[
                                                                          html.Div(
                                                                              className='legend_icon_blue'),
                                                                          'Ongoing']),
                                                         ])
                                            ]),
                                   html.Div(className='center_column',
                                            children=[
                                                html.Div(className='top_box',
                                                         children=html.Div(className='general_text_container',
                                                                           children=[
                                                                               html.Div(className='general_text',
                                                                                        children='Total Studies:'),
                                                                               html.Div(
                                                                                   className='general_number',
                                                                                   children=html.Div(
                                                                                       className='stats-container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               id='TotalStudies_Val'),
                                                                                           html.Img(
                                                                                               id='TotalStudies',
                                                                                               className='arrow'
                                                                                           )
                                                                                       ]))
                                                                           ])
                                                         ),
                                                html.Div(className='middle_box',
                                                         children=[
                                                             html.Div(className='donut',
                                                                      children=dcc.Graph(id='pie_plot'))
                                                         ]),
                                                html.Div(className='bottom_box',
                                                         children=html.Div(children=dcc.Graph(id='stacked_bar')))
                                            ]),
                                   html.Div(className='right_column',
                                            children=[
                                                html.Div(className='right_top_container',
                                                         children=[
                                                             html.Div(className='right_top_blue_box',
                                                                      children=html.Div(
                                                                          className='general_text_container',
                                                                          children=[
                                                                              html.Div(className='general_text',
                                                                                       children='Total EDC Builds:'),
                                                                              html.Div(
                                                                                  className='general_number',
                                                                                  children=html.Div(
                                                                                      className='stats-container',
                                                                                      children=[
                                                                                          html.Div(
                                                                                              id='EDCBuilds_Val'),
                                                                                          html.Img(
                                                                                              id='EDCBuilds',
                                                                                              className='arrow')]))
                                                                          ])
                                                                      ),
                                                             html.Div(className='right_top_orange_box',
                                                                      children=html.Div(
                                                                          className='general_text_container',
                                                                          children=[
                                                                              html.Div(className='general_text',
                                                                                       children='Total EDC DBLs:'),
                                                                              html.Div(
                                                                                  className='general_number',
                                                                                  children=html.Div(
                                                                                      className='stats-container',
                                                                                      children=[
                                                                                          html.Div(
                                                                                              id='DBL_Val'),
                                                                                          html.Img(
                                                                                              id='DBL',
                                                                                              className='arrow')]))
                                                                          ])
                                                                      ),
                                                             html.Div(className='right_top_green_box',
                                                                      children=html.Div(
                                                                          className='general_text_container',
                                                                          children=[
                                                                              html.Div(className='general_text',
                                                                                       children='Total Analyses:'),
                                                                              html.Div(
                                                                                  className='general_number',
                                                                                  children=html.Div(
                                                                                      className='stats-container',
                                                                                      children=[
                                                                                          html.Div(
                                                                                              id='FinalTFL_Val'),
                                                                                          html.Img(
                                                                                              id='FinalTFL',
                                                                                              className='arrow')]))
                                                                          ])
                                                                      )
                                                         ]),
                                                html.Div(className='right_bottom_container',
                                                         children=[
                                                             html.Div(className='text_container',
                                                                      children='Timeliness'),
                                                             html.Div(className='box_container',
                                                                      children=[
                                                                          html.Div(className='blue_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='Protocol to EDC:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='PROTtoEDC_Val'),
                                                                                                       html.Img(
                                                                                                           id='PROTtoEDC_Median',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='orange_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='LPLV to DBL:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='LPLVtoDBL_Val'),
                                                                                                       html.Img(
                                                                                                           id='LPLVtoDBL_Median',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='green_box',
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='DBL to TFL:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='DBLtoTFL_Val'),
                                                                                                       html.Img(
                                                                                                           id='DBLtoTFL_Median',
                                                                                                           className='arrow')]))])
                                                                                   )
                                                                      ]),
                                                             html.Div(className='text_container',
                                                                      children='Quantity'),
                                                             html.Div(className='box_container',
                                                                      children=[
                                                                          html.Div(className='blue_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='# of eCRFs:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumCRF_Val'),
                                                                                                       html.Img(
                                                                                                           id='NumCRF_Median',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='orange_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='# of Queries:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumQueries_Val'),
                                                                                                       html.Img(
                                                                                                           id='NumQueries_Median',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='green_box',
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='# of TFLs:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumTFLs_Val'),
                                                                                                       html.Img(
                                                                                                           id='NumTFLs_Median',
                                                                                                           className='arrow')]))])
                                                                                   )
                                                                      ]),
                                                             html.Div(className='text_container',
                                                                      children='Quality'),
                                                             html.Div(className='box_container',
                                                                      children=[
                                                                          html.Div(className='blue_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='Migration <= 2:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumMigrationLE2_val'),
                                                                                                       html.Img(
                                                                                                           id='NumMigrationLE2_perc',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='orange_box',
                                                                                   style={'margin-right': '34px'},
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='Study with DBUL:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumStudyDBUL_val'),
                                                                                                       html.Img(
                                                                                                           id='NumStudyDBUL_n',
                                                                                                           className='arrow')]))])
                                                                                   ),
                                                                          html.Div(className='green_box',
                                                                                   children=html.Div(
                                                                                       className='general_text_container',
                                                                                       children=[
                                                                                           html.Div(
                                                                                               className='general_text',
                                                                                               children='TFL <= 250:'),
                                                                                           html.Div(
                                                                                               className='general_number',
                                                                                               children=html.Div(
                                                                                                   className='stats-container',
                                                                                                   children=[
                                                                                                       html.Div(
                                                                                                           id='NumTFLsLE250_val'),
                                                                                                       html.Img(
                                                                                                           id='NumTFLsLE250',
                                                                                                           className='arrow')]))])
                                                                                   )
                                                                      ]),
                                                         ])
                                            ]),
                               ])
                  ])


@callback(
    Output('pie_plot', 'figure'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_donut_plot(current_year, selected_TA, selected_phase):
    df_filter = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)
    df_filter = df_filter[df_filter['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter = df_filter[df_filter['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total = df_filter.at[0, 'TotalStudies']

    # Create the donut plot
    fig = go.Figure(
        data=[go.Pie(
            labels=df_filter['Status'],
            values=df_filter['StatusCount'],
            hole=0.7,
            marker=dict(colors=['#77b7b3', '#e15759', '#4f7aa7']),
            textfont=dict(color='white'),
            textinfo='value',
            textposition='outside',
            hovertemplate=
            'Status: <b>%{label}</b>' +
            '<br>Studies: <b>%{value}</b>',
        )],

        layout=go.Layout(
            title="Study Status",
            title_font=dict(color='white'),
            margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False,
            annotations=[dict(text=f"Studies:{total}", x=0.50, y=0.5, font_size=15, showarrow=False,
                              font=dict(color='white'))],
            paper_bgcolor='#262F3D',
            height=230,
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial")
        )
    )
    return fig


@callback(
    Output('stacked_bar', 'figure'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value'),
)
def update_bar_plot(current_year, selected_TA, selected_Phase):
    df_filter = df_sonar_simple[df_sonar_simple['TA'] == selected_TA]
    df_filter = df_filter[df_filter['Year'] == current_year][['Phase', 'StatusCount', 'Status']]
    df_filter = df_filter[df_filter['Phase'].str.contains('All') == False]
    df_filter = df_filter.sort_values(by='Phase', ascending=True)

    if selected_Phase == 'All':
        fig = px.bar(x=df_filter['Phase'],
                     y=df_filter['StatusCount'],
                     color=df_filter['Status'],
                     text=df_filter['StatusCount'].astype(str),
                     color_discrete_sequence=['#77b7b3', '#e15759', '#4f7aa7'],
                     category_orders={'Status': ["P3", "P2", "P1"]},
                     )
        fig.update_traces(
            textfont=dict(color='white'),
            width=0.5,
            marker_line_width=0,
            hovertemplate=
            'Phase: <b>%{x}</b>' +
            '<br>Studies: <b>%{y}</b>'
        )
        fig.update_layout(
            title="Status by Phase",
            title_font=dict(color='white'),
            paper_bgcolor='#262F3D',
            plot_bgcolor='#262F3D',
            height=240,
            width=245,
            showlegend=False,
            xaxis_title='',
            yaxis_title='',
            margin=dict(l=0, r=20, t=60, b=0),
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            xaxis_tickfont_color='white',
            xaxis=dict(zeroline=False),
            hoverlabel=dict(
                bgcolor="white",
                font_size=12,
                font_family="Arial")
        )
        fig.update_yaxes(showticklabels=False,
                         showgrid=False,
                         zerolinecolor='rgba(0,0,0,0)'
                         )

    else:
        df_filter = df_filter[df_filter['Phase'] == selected_Phase]
        fig = px.bar(x=df_filter['Phase'],
                     y=df_filter['StatusCount'],
                     color=df_filter['Status'],
                     text=df_filter['StatusCount'].astype(str),
                     color_discrete_sequence=['#77b7b3', '#e15759', '#4f7aa7'],
                     category_orders={'Status': df_filter['Phase'].unique()})
        fig.update_traces(
            textfont=dict(color='white'),
            width=0.5,
            marker_line_width=0
        )
        fig.update_layout(
            title="Status by Phase",
            title_font=dict(color='white'),
            paper_bgcolor='#262F3D',
            plot_bgcolor='#262F3D',
            height=240,
            width=245,
            showlegend=False,
            xaxis_title='',
            yaxis_title='',
            margin=dict(l=0, r=20, t=60, b=0),
            xaxis_showgrid=False,
            yaxis_showgrid=False,
            xaxis_tickfont_color='white',
            xaxis=dict(zeroline=False)
        )
        fig.update_yaxes(showticklabels=False,
                         showgrid=False,
                         zerolinecolor='rgba(0,0,0,0)'
                         )
    return fig


'''
The section below are callback functions that drive the main data display based on user parameter selections.
Each Cell has three callback sections:
1. The value callback that displays the value given the parameters
2. The arrow callback that determines which arrow icon to display
3. The hover callback that displays the value difference between current and compared year
'''

# arrow icon sources:
up_arrow = 'assets/green_up.png'
down_arrow = 'assets/red_down.png'
equal_dash = 'assets/dash.png'


# Total Studies:
@callback(
    Output('TotalStudies_Val', 'children'),
    Output('TotalStudies', 'src'),
    Output('TotalStudies', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'TotalStudies']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'TotalStudies']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return total_year, up_arrow, f'Total Studies - Change: {change}'
    elif total_year == total_year_compared:
        return total_year, equal_dash, f'Total Studies - Change: {change}'
    else:
        return total_year, down_arrow, f'Total Studies - Change: {change}'


# Total EDC Builds:
@callback(
    Output('EDCBuilds_Val', 'children'),
    Output('EDCBuilds', 'src'),
    Output('EDCBuilds', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'EDCBuilds']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'EDCBuilds']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return total_year, up_arrow, f'EDC Builds - Change: {change}'
    elif total_year == total_year_compared:
        return total_year, equal_dash, f'EDC Builds - Change: {change}'
    else:
        return total_year, down_arrow, f'EDC Builds - Change: {change}'


# FinalEDC_DBL:
@callback(
    Output('DBL_Val', 'children'),
    Output('DBL', 'src'),
    Output('DBL', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'DBL']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'DBL']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return total_year, up_arrow, f'Total Final DBL - Change: {change}'
    elif total_year == total_year_compared:
        return total_year, equal_dash, f'Total Final DBL - Change: {change}'
    else:
        return total_year, down_arrow, f'Total Final DBL - Change: {change}'


# FinalTFL:
@callback(
    Output('FinalTFL_Val', 'children'),
    Output('FinalTFL', 'src'),
    Output('FinalTFL', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'FinalTFL']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'FinalTFL']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return total_year, up_arrow, f'Total Final Analyses - Change: {change}'
    elif total_year == total_year_compared:
        return total_year, equal_dash, f'Total Final Analyses - Change: {change}'
    else:
        return total_year, down_arrow, f'Total Final Analyses - Change: {change}'


# PROTtoEDC:
# Value
@callback(
    Output('PROTtoEDC_Val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'PROTtoEDC_Median']

    return total_year


# Arrow
@callback(
    Output('LPLVtoDBL_Val', 'children'),
    Output('PROTtoEDC_Median', 'src'),
    Output('PROTtoEDC_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'PROTtoEDC_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'PROTtoEDC_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return total_year, up_arrow, f'Protocol to EDC (Median Days) - Change: {change}'
    elif total_year == total_year_compared:
        return total_year, equal_dash, f'Protocol to EDC (Median Days) - Change: {change}'
    else:
        return total_year, down_arrow, f'Protocol to EDC (Median Days) - Change: {change}'


# Arrow
@callback(
    Output('LPLVtoDBL_Median', 'src'),
    Output('LPLVtoDBL_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'LPLVtoDBL_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'LPLVtoDBL_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'LPLV to DBL (Median Days) - Change: {change}'
    elif total_year == total_year_compared:
        return equal_dash, f'LPLV to DBL (Median Days) - Change: {change}'
    else:
        return down_arrow, f'LPLV to DBL (Median Days) - Change: {change}'


# DBLtoTFL:
# Value
@callback(
    Output('DBLtoTFL_Val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'DBLtoTFL_Median']

    return total_year


# Arrow
@callback(
    Output('DBLtoTFL_Median', 'src'),
    Output('DBLtoTFL_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'DBLtoTFL_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'DBLtoTFL_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'DBL 2 TFL (Median Days): {change}'
    elif total_year == total_year_compared:
        return equal_dash, f'DBL 2 TFL (Median Days): {change}'
    else:
        return down_arrow, f'DBL 2 TFL (Median Days): {change}'


# eCRFs:
# Value
@callback(
    Output('NumCRF_Val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumCRF_Median']

    return total_year


# Arrow
@callback(
    Output('NumCRF_Median', 'src'),
    Output('NumCRF_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumCRF_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumCRF_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'# of eCRF (Median) - Change: {change}'
    elif total_year == total_year_compared:
        return equal_dash, f'# of eCRF (Median) - Change: {change}'
    else:
        return down_arrow, f'# of eCRF (Median) - Change: {change}'


# Queries:
# Value
@callback(
    Output('NumQueries_Val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumQueries_Median']

    return total_year


# Arrow
@callback(
    Output('NumQueries_Median', 'src'),
    Output('NumQueries_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumQueries_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumQueries_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'# of Queries (Median) - Change: {change}'
    elif total_year == total_year_compared:
        return equal_dash, f'# of Queries (Median) - Change: {change}'
    else:
        return down_arrow, f'# of Queries (Median) - Change: {change}'


# TFLs:
# Value
@callback(
    Output('NumTFLs_Val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumTFLs_Median']

    return total_year


# Arrow
@callback(
    Output('NumTFLs_Median', 'src'),
    Output('NumTFLs_Median', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumTFLs_Median']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumTFLs_Median']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'# of TFLs (Median) - Change: {change}'
    elif total_year == total_year_compared:
        return equal_dash, f'# of TFLs (Median) - Change: {change}'
    else:
        return down_arrow, f'# of TFLs (Median) - Change: {change}'


# Migration:
# Value
@callback(
    Output('NumMigrationLE2_val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumMigrationLE2_perc']

    return f'{round(total_year * 100, 1)}%'


# Arrow
@callback(
    Output('NumMigrationLE2_perc', 'src'),
    Output('NumMigrationLE2_perc', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumMigrationLE2_perc']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumMigrationLE2_perc']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'Migration<=2% - Change: {change}%'
    elif total_year == total_year_compared:
        return equal_dash, f'Migration<=2% - Change: {change}%'
    else:
        return down_arrow, f'Migration<=2% - Change: {change}%'


# DBUL:
# Value
@callback(
    Output('NumStudyDBUL_val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumStudyDBUL_perc']

    return f'{round(total_year * 100, 1)}%'


# Arrow
@callback(
    Output('NumStudyDBUL_n', 'src'),
    Output('NumStudyDBUL_n', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumStudyDBUL_perc']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumStudyDBUL_perc']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'Study with DBUL% - Change: {change}%'
    elif total_year == total_year_compared:
        return equal_dash, f'Study with DBUL% - Change: {change}%'
    else:
        return down_arrow, f'Study with DBUL% - Change: {change}%'


# TFL <= 250:
# Value
@callback(
    Output('NumTFLsLE250_val', 'children'),
    Input('current-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumTFLsLE250_perc']

    return f'{round(total_year * 100, 1)}%'


# Arrow
@callback(
    Output('NumTFLsLE250', 'src'),
    Output('NumTFLsLE250', 'title'),
    Input('current-year', 'value'),
    Input('compared-year', 'value'),
    Input('selected-TA', 'value'),
    Input('selected-phase', 'value')
)
def update_output(current_year, compared_year, selected_TA, selected_phase):
    df_temp = df_sonar_simple[df_sonar_simple['TA'] == selected_TA].reset_index().drop('index', axis=1)

    df_filter_current = df_temp[df_temp['Year'] == current_year].reset_index().drop('index', axis=1)
    df_filter_current = df_filter_current[df_filter_current['Phase'] == selected_phase].reset_index().drop('index',
                                                                                                           axis=1)
    total_year = df_filter_current.at[0, 'NumTFLsLE250_perc']

    df_filter_comp = df_temp[df_temp['Year'] == compared_year].reset_index().drop('index', axis=1)
    df_filter_comp = df_filter_comp[df_filter_comp['Phase'] == selected_phase].reset_index().drop('index', axis=1)
    total_year_compared = df_filter_comp.at[0, 'NumTFLsLE250_perc']

    change = total_year - total_year_compared

    if total_year > total_year_compared:
        return up_arrow, f'Study with TFL<=250% - Change: {change}%'
    elif total_year == total_year_compared:
        return equal_dash, f'Study with TFL<=250% - Change: {change}%'
    else:
        return down_arrow, f'Study with TFL<=250% - Change: {change}%'
