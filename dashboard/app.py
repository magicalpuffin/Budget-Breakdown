import dash
from dash import html
import dash_bootstrap_components as dbc

from components.navbar import navbar

# Sets the theme, don't actually remember why it uses dbc.
# Initializes the actual dash object. Not sure if there is a point of separting this from content
external_stylesheets = [dbc.themes.BOOTSTRAP, "./assets/typography.css"]
app = dash.Dash(
    __name__,
    use_pages= True,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
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
