from dashboard.index import app
from dash import html, dcc, dash_table
import pandas as pd
import plotly.express as px
from dash import Input, Output
import json

credit_categorized_df = pd.read_csv('credit_categorized.csv')
credit_categorized_df["Date"] = pd.to_datetime(credit_categorized_df["Date"])

# grouped_df = credit_categorized_df.groupby([pd.Grouper(key= "Date", axis= 0, freq= "M"), "Name", "Type"]).sum()
# grouped_df = grouped_df.reset_index()
grouped_df = credit_categorized_df

# fig = px.bar(spending_df, x="Date", y="Amount", color="Type")
fig = px.histogram(grouped_df, x="Date", y="Amount", color="Type", hover_name= "Name")
fig.update_traces(xbins = dict(size = 'M1'))
fig.update_layout(bargap = 0.2)
fig.update_xaxes(ticklabelmode = 'period')

filter_col = 'Type'
filter_vals = pd.DataFrame({'item_name': grouped_df[filter_col].unique()})
filter_vals['filter'] = True

budget_tab = html.Div(
    [
        html.Div(
            [
                html.H5('Budget Breakdown Figure'),
                dcc.Graph(id= 'budget-fig', figure= fig),
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
                html.H5('Import Data')
            ]
        )
    ]
)

@app.callback(
    Output('selected-data', 'children'),
    Output('budget-table', 'data'),
    Input('budget-fig', 'restyleData')
)
def display_click_data(restyleData):
    if restyleData:
        legend_change = pd.DataFrame({'filter': restyleData[0]['visible']}, index = restyleData[1])
        legend_change['filter'][legend_change['filter'] == 'legendonly'] = False

        filter_vals.update(legend_change)

    filter_array = filter_vals[filter_vals['filter']]['item_name'].values
    filtered_data = credit_categorized_df[credit_categorized_df['Type'].isin(filter_array)]
    filtered_data = filtered_data.to_dict('records')
    debugtext = html.Div(
        [
            json.dumps(restyleData, indent=2),
            html.Div(filter_array)

        ]
    )
    return debugtext, filtered_data