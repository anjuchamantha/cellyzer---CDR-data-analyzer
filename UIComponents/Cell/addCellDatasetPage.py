import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

from simpleTitleBar import SimpleTitleBar


def AddCellDatasetPage():
    navbar = SimpleTitleBar(name="Add Cell DataSet")

    data_set_input = dbc.FormGroup(
        [
            dbc.Label("Cell DataSet File path", width=2),
            dbc.Col(
                dbc.Input(
                    id="cell-dataSet-input", placeholder="Ex:   D:\datasets\cell.csv"
                ),
            ),

        ],
        row=True,
    )
    data_set_name = dbc.FormGroup(
        [
            dbc.Label("Cell Dataset Name", width=2),
            dbc.Col(
                dbc.Input(
                    id="cell-dataSet-name-input", placeholder="How do you want to call this dataset?"
                ),
            ),

        ],
        row=True,
    )

    call_dataset = dbc.FormGroup(
        [
            dbc.Label("Select the Call Dataset to link", width=2),
            dbc.Col(
                dbc.DropdownMenu(
                    label="Select Call Dataset",
                    children=[
                        dbc.DropdownMenuItem("Call Dataset 1"),
                        dbc.DropdownMenuItem("Call Dataset 2"),
                        dbc.DropdownMenuItem("Call Dataset 3"),
                    ],
                )
            ),

        ],
        row=True,
    )

    form = dbc.Form([data_set_input, data_set_name, call_dataset])

    content = html.Div(
        [dbc.Row(
            [
                dbc.Col(dbc.Alert("Note : You need to link a Call Dataset in-order to add a Cell/Antenna Dataset",
                                  color="danger"), width=10),
                dbc.Col(dbc.Button("Add NEW Call DataSet", color="danger", size="lg", className="mr-1",
                                   style={"margin-bottom": 50}, href="/add_call_dataset"), width=2),
            ],

        ),

            form,
            dbc.Button("Add DataSet", color="primary", className="mr-1 float-right", href="/dataset"),
        ],
        style={"margin": 20, "margin-top": 100, }

    )

    return html.Div(children=[content, navbar])
