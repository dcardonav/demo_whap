

from dash import Dash, Input, Output, State, html, dcc

import pandas as pd
import plotly.express as px

happiness = pd.read_csv('data/world_happiness.csv')
app = Dash()  # create Dash app

# now to define the layout of the dashboard
app.layout = html.Div(children=[  # adding a list of components as children of the div
    html.H1(children='World Happiness Dashboard'),
    html.P(['This dashboard shows the happiness score.',
            html.Br(),
            html.A('World Happiness Report Data Source',
                   href='https://worldhappiness.report',
                   target='_blank')]),  # open in new webpage

    dcc.RadioItems(id='region_radio',
                   options=happiness['region'].unique(),
                   value='North America'),  # default selected option

    dcc.Dropdown(id='country_dropdown'),

    dcc.RadioItems(id='data_radio', options={
                        # the keys are what is sent in the callback function, the values are
                        # what is shown to the user
                        'happiness_score': 'Happiness Score',
                        'happiness_rank': 'Happiness Rank'
                    },
                   value='happiness_score'),  # default selected option

    html.Br(),
    dcc.Graph(id='happiness_graph'), # previously created lineplot
    html.Div(id='average_div')
])

@app.callback(
    Output(component_id='country_dropdown', component_property='options'),
    Output(component_id='country_dropdown', component_property='value'),
    Input(component_id='region_radio', component_property='value')
)
def update_region(selected_region):
    filtered_happiness = happiness[happiness['region'] == selected_region]
    country_options = filtered_happiness['country'].unique()

    return country_options, country_options[0]  # returns the first country of the region


@app.callback(
    Output(component_id='happiness_graph', component_property='figure'),
    Output(component_id='average_div', component_property='children'),
    Input(component_id='country_dropdown', component_property='value'),
    Input(component_id='data_radio', component_property='value')
)

def update_graph(selected_country, selected_data):
    filtered_happiness = happiness[happiness['country'] == selected_country]

    # the y-axis changes based on the chosen metric in the dashboard
    line_fig = px.line(filtered_happiness, x='year', y=selected_data,
                       title=f'{selected_data} in {selected_country}')

    selected_average = filtered_happiness[selected_data].mean()

    return line_fig, f'The average {selected_data} for {selected_country} is {selected_average}'

if __name__ == '__main__':

    # running the dashboard's server
    app.run_server(debug=True) # similar to Flask
