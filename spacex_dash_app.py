# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Br(),
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                        {'label': 'All Sites', 'value': 'All Sites'}],
                                    value='All Sites', 
                                    placeholder="Select a Launch Site here"),
                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Br(),
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                html.Div(dcc.RangeSlider(id='payload-slider', min = 0, max = 10000, step=1000, value=[min_payload,max_payload])),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
            Output(component_id='success-pie-chart', component_property='figure'), 
            Input(component_id='site-dropdown', component_property='value'))

def generate_pie_chart(site_dropdown):
    
    if site_dropdown == 'All Sites':
        pie_chart = px.pie(spacex_df, values='class', names='Launch Site', title='Launch Success Counts')
    else:
        spacex_df_mod = spacex_df.loc[spacex_df['Launch Site']==site_dropdown]
        pie_chart = px.pie(spacex_df_mod ,values=spacex_df_mod['class'].value_counts().values, names=spacex_df_mod['class'].value_counts().index, title='Launch Success Counts')
    
    pie_chart.update_layout()
    return pie_chart                           
                                
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
            Output(component_id='success-payload-scatter-chart', component_property='figure'), 
            [Input(component_id='site-dropdown', component_property='value'), 
            Input(component_id="payload-slider", component_property="value")])

def generate_scatter_chart(site_dropdown,rangevalue):
    
    if site_dropdown == 'All Sites':
        spacex_df_mod2 = spacex_df.loc[(spacex_df['Payload Mass (kg)']>=rangevalue[0]) 
                                        & (spacex_df['Payload Mass (kg)']<=rangevalue[1])]

        scatter_chart = px.scatter(spacex_df_mod2, x='Payload Mass (kg)', y='class', color="Booster Version Category", title='Scatter Plot for Launch Success Counts')
    else:
        spacex_df_mod3 = spacex_df.loc[(spacex_df['Launch Site']==site_dropdown) 
                                        & (spacex_df['Payload Mass (kg)']>=rangevalue[0]) 
                                        & (spacex_df['Payload Mass (kg)']<=rangevalue[1])]
        
        scatter_chart = px.scatter(spacex_df_mod3, x='Payload Mass (kg)', y='class', color="Booster Version Category", title='Scatter Plot for Launch Success Counts')
        
    scatter_chart.update_layout()
    return scatter_chart                           


# Run the app
if __name__ == '__main__':
    app.run_server()
