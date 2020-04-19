import dash_bootstrap_components as dbc
import dash_html_components as html

def NavBar():
    return html.Div(
        dbc.NavbarSimple(
            children=[
                dbc.Button("Overview", color="secondary", size="sm", style={"margin": 4}),
                dbc.Button("Add DataSet", color="success", size="sm", style={"margin": 4}),
            ],
            brand="DataSets",
            brand_href="#",
            color="dark",
            dark=True,
            fluid=True,
            # sticky=True,

        ),
        style={
            "padding-top": 20,
            "padding-bottom": 20,
            "position": "fixed",
            "overflow": "hidden",
            "top": 0,
            "width": "100rem",
            "background-color": "white",
        }
    )