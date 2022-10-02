import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path='/',
    redirect_from=['/home'],
    title='Home'
)

layout = html.Div(
    [
        dcc.Markdown('''
        #### Home Page

        Using Markdown because it is easier to use and format in dash.
        
        This is a basic page for testing. The objective is to be able to create and append
        a personal budget. This webapp is also used for experimentation on how to use plotly.

        ''')
    ]
)