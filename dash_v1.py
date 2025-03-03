import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import numpy as np

opnrcd_full_df = pd.read_csv('source_data/OPNRCD_alltime_stats.csv')
opnrcd_df = opnrcd_full_df[opnrcd_full_df["Strophe?"]]  # Strophen only

def extract_years(df):
    years = df['Jahr'].unique()
    years.sort()
    years = np.append(years, np.array(['All']))
    years = years[::-1]
    return years

years = extract_years(opnrcd_df)

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.Div([dcc.Dropdown(id='year-select', options=[{'label': i, 'value': i} for i in years],
                           value='All', style={'width': '140px'})]),
    dcc.Graph('scatterplot', config={'displayModeBar': False})])


@app.callback(
    Output('scatterplot', 'figure'),
    [Input('year-select', 'value')]
)
def update_graph(year):
    import plotly.express as px
    df_for_plot = opnrcd_df[opnrcd_df['Jahr'] == int(year)] if year != 'All' else opnrcd_df
    fig = px.scatter(df_for_plot, x='Künstlerische Relevanz (1-10)', y='Musikalische Härte (1-10)',
                      size='Dauer (s)', color='Jahr')
    fig.update_layout(transition_duration=200)
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
