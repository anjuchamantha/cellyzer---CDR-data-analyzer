import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc

from simpleTitleBar import SimpleTitleBar


def HomePage():
    navbar = SimpleTitleBar(name="Cellyzer Home Page")
    content = html.Div(
        children=[
            dbc.Jumbotron(
                [
                    html.H1("Cellyzer", className="display-3"),
                    html.P(
                        "CELLYZER is a library to analyze "
                        "Call Detail Records.",
                        className="lead",
                    ),
                    html.Hr(className="my-2"),
                    html.P(
                        "View the documentation for more details. "
                    ),
                    html.P(dbc.Button("Visit Project Repository", color="primary"), className="lead"),
                ]
            )
        ],
        style={"margin": 20, "margin-top": 70, }

    )

    return html.Div(children=[content,])
