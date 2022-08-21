from dash import Dash
import dash_bootstrap_components as dbc

# Sets the theme, don't actually remember why it uses dbc.
external_stylesheets = [dbc.themes.BOOTSTRAP, "./assets/typography.css"]
app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=external_stylesheets,
)

app_title = "Budget Breakdown"