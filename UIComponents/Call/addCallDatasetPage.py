import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

from simpleTitleBar import SimpleTitleBar


def AddCallDatasetPage():
    navbar = SimpleTitleBar(name="Add Call DataSet")
    data_set_input = dbc.FormGroup(
        [
            dbc.Label("Call DataSet File path", width=2),
            dbc.Col(
                dbc.Input(
                    id="call-dataSet-input", placeholder="Ex:   D:\datasets\calls.csv"
                ),
            ),

        ],
        row=True,
    )
    data_set_name = dbc.FormGroup(
        [
            dbc.Label("Call Dataset Name", width=2),
            dbc.Col(
                dbc.Input(
                    id="call-dataSet-name-input", placeholder="How do you want to call this dataset?"
                ),
            ),

        ],
        row=True,
    )

    form = dbc.Form([data_set_input, data_set_name])

    content = html.Div(
        [
            form,
            dbc.Button("Add DataSet", color="primary", className="mr-1 float-right", href="/dataset"),
        ],
        style={"margin": 20, "margin-top": 100, }

    )

    return html.Div(children=[content, navbar])
