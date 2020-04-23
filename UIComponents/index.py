import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from Call.callPage import CallPage
from DataSetPage.datasetPage import DataSetPage

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}


# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "16rem",
    "padding": 20,
}

sidebar = html.Div(
    [
        html.H2("CELLYZER", className="display-6", style={"text-align": "center"}),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/home", id="home"),
                dbc.NavLink("DataSets", href="/demo_datasets", id="demo_datasets"),
                dbc.NavLink("Analytics", href="/analytics", id="analytics"),

            ],
            vertical=True,
            pills=True,
        ),

    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"{i}", "active") for i in ["home", "demo_datasets", "analytics"]],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/" or pathname == "/home":
        # Treat page 1 as the homepage / index
        return True, False, False
    if pathname == "/demo_datasets":
        return False, True, False
    if pathname == "/analytics":
        return False, False, True


datasetpage = DataSetPage()


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname in ["/", "/home"]:
        return html.P("HomePage")
    elif pathname == "/demo_datasets":
        return datasetpage
    elif pathname == "/analytics":
        return html.P("Analytics Page")
    elif pathname == "/demo_datasets/call":
        return CallPage()


    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


if __name__ == "__main__":
    app.run_server(port=8888)
