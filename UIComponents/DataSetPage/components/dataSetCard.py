import dash_bootstrap_components as dbc
import dash_html_components as html


def DataSetCard(name, records="-", type="call"):
    return dbc.Card(
        children=[
            dbc.CardHeader(html.H5(name, style={"text-align": "center"})),
            dbc.CardBody(
                [
                    html.H5(records, style={"font-size": 50, "margin-bottom": 0}),
                    html.P(
                        "records", style={}
                    ),
                    html.Br(),
                    dbc.Button("Visit DataSet", color="primary", href="/dataset/" + type),
                ],
                style={"text-align": "center", "height": 220}
            ),
        ],
        style={"width": 300, "margin-right": 20, "margin-bottom": 20, }
    )


def AddDataSetCard(d_type="call"):
    url = ""
    if d_type == "call":
        url = "/add_call_dataset"
    elif d_type == "message":
        url = "/add_message_dataset"
    elif d_type == "cell":
        url = "/add_cell_dataset"
    return dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Button("+", color="secondary", outline=True, href=url,
                               style={"font-size": 140, "height": 260, "width": 260
                                      }),
                ],
            ),
        ],
        style={"margin-bottom": 20, "width": 300}
    )
