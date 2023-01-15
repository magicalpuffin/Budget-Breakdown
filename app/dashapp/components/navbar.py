import dash_bootstrap_components as dbc

# Generates navbar, appends pages to the base url
def navbar(baseurl:str) -> dbc.NavbarSimple:
    layout = dbc.NavbarSimple([
        # html.Img(src= dash.get_asset_url('images/logo.png'), height= "30px", className= "mx-3"),
        dbc.NavItem(dbc.NavLink("Home", href= baseurl)),
        dbc.DropdownMenu([
            dbc.DropdownMenuItem("2022 Report", href= baseurl + '2022-report'),
        ], nav= True, in_navbar= True, label= 'Reports'),
        dbc.NavItem(dbc.NavLink("View Budget", href= baseurl + 'view-budget')),
        dbc.NavItem(dbc.NavLink("Append Budget", href= baseurl + 'append-budget')),
        dbc.NavItem(dbc.NavLink("Edit Types", href= baseurl + 'edit-types')),
    ],
    links_left= True
    )

    return layout