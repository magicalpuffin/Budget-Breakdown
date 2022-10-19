import dash
from dash import html
import dash_bootstrap_components as dbc

from components.navbar import navbar

app = dash.Dash(
    __name__,
    use_pages= True,
    suppress_callback_exceptions=True,
    title= "Budget Breakdown"
)

app.layout = html.Div(children=
    [
        navbar,
        dash.page_container
    ]
)

sever = app.server

if __name__ == "__main__":
    app.run_server(debug = True)
