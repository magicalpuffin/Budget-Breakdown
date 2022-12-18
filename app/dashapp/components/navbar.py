import dash_bootstrap_components as dbc

# Generates navbar, appends pages to the base url
def navbar(baseurl):
    layout = dbc.NavbarSimple(
        children= [
            dbc.NavItem(dbc.NavLink("Home", href= baseurl)),
            dbc.NavItem(dbc.NavLink("View Budget", href= baseurl + 'view-budget')),
            dbc.NavItem(dbc.NavLink("Append Budget", href= baseurl + 'append-budget')),
            dbc.NavItem(dbc.NavLink("Edit Types", href= baseurl + 'edit-types')),
        ],
        links_left= True
    )
    return layout