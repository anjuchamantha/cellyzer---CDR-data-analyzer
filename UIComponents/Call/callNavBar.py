import dash_bootstrap_components as dbc
import dash_html_components as html


def CallNavBar(name="<Dataset Name>"):
    return html.Div(
        dbc.NavbarSimple(
            children=[
                dbc.Button("View DataSet", color="secondary", size="sm", style={"margin": 4}),
                dbc.Button("Functions", color="warning", size="sm", style={"margin": 4}),
            ],
            brand="Call DataSet : " + name,
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
