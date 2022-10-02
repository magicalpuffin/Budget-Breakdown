import dash_bootstrap_components as dbc

navbar= dbc.NavbarSimple(
    children= [
        dbc.NavItem(dbc.NavLink("Home", href='/')),
        dbc.NavItem(dbc.NavLink("View Budget", href='/view-budget')),
        dbc.NavItem(dbc.NavLink("Append Budget", href='/append-budget')),
        dbc.NavItem(dbc.NavLink("Edit Types", href='/edit-types')),
    ],
    links_left= True
)