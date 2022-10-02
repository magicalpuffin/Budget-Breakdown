import dash
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
from dash import callback, Input, Output
import json

# Currently this is just for testing displaying data
# Creates a figure and displays in web app
# Use of csv and transfering data should be figured out. Use a datafolder, parquets, readwrite functions?

dash.register_page(
    __name__,
    path= '/view-budget',
    title= 'View Budget'
)

credit_categorized_df = pd.read_csv('credit_categorized.csv')
credit_categorized_df["Date"] = pd.to_datetime(credit_categorized_df["Date"])
# Initializes filter_vals
filter_col = 'Type'
filter_vals = pd.DataFrame({'item_name': credit_categorized_df[filter_col].unique()})
filter_vals['filter'] = True

layout = html.Div(
    [
        html.Div(
            [
                html.H5('Budget Breakdown Figure', id= 'main-header'),
                dcc.Graph(id= 'budget-fig'),
                dash_table.DataTable(
                    id = 'budget-table',
                    data = credit_categorized_df.to_dict('records'), 
                    columns = [{"name": i, "id": i} for i in credit_categorized_df.columns], 
                    style_table={'height': '300px', 'overflowY': 'auto'},
                    page_size=20,
                    fixed_rows={'headers': True}
                ),
                html.Pre(id='selected-data')
            ]
        ),
        html.Div(
            [
                html.H5(id= 'debug-text')
            ]
        )
    ]
)

@callback(
    Output('budget-fig', 'figure'),
    Input('main-header', 'children')
)
def load_fig(header_text):
    credit_categorized_df = pd.read_csv('dashboard/data/credit_categorized.csv')
    credit_categorized_df["Date"] = pd.to_datetime(credit_categorized_df["Date"])

    # fig is generated before rendering rest of tab
    fig = px.histogram(credit_categorized_df, x="Date", y="Amount", color="Type", hover_name= "Name")
    fig.update_traces(xbins = dict(size = 'M1'))
    fig.update_layout(bargap = 0.2)
    fig.update_xaxes(ticklabelmode = 'period')
    
    return fig

@callback(
    Output('selected-data', 'children'),
    Output('budget-table', 'data'),
    Input('budget-fig', 'restyleData')
)
def display_click_data(restyleData):
    # Function that adjusts table display whenever restyleData is interacted with
    # restlyData outputs a json transitioning from previous to new state based on legend selection
    if restyleData:
        # legend_change is a bool df indexed on legend. True False indicated if each legend was selected or not 
        legend_change = pd.DataFrame({'filter': restyleData[0]['visible']}, index = restyleData[1])
        legend_change['filter'][legend_change['filter'] == 'legendonly'] = False

        # filter_vals is updated based on the changes, no change means no index is updated
        filter_vals.update(legend_change)

    # Converts the filter_vals dataframe into an array to filter the dataset
    filter_array = filter_vals[filter_vals['filter']]['item_name'].values
    filtered_data = credit_categorized_df[credit_categorized_df['Type'].isin(filter_array)]
    filtered_data = filtered_data.to_dict('records')
    
    # Creates debug text, non essential
    debugtext = html.Div(
        [
            json.dumps(restyleData, indent=2),
            html.Div(filter_array)

        ]
    )
    return debugtext, filtered_data