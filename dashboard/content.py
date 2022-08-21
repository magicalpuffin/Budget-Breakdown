from dashboard.index import app
from dashboard.layout.budget_tab import budget_tab
from dashboard.layout.callbacks import budget_tab_callback
from dash import dcc, html
import dash_bootstrap_components as dbc

app.layout = html.Div(
    [
        budget_tab
    ]
)