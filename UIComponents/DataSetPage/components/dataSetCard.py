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
                    dbc.Button("Visit DataSet", color="primary", href="/demo_datasets/" + type),
                ],
                style={"text-align": "center"}
            ),
        ],
        style={"width": 300, "margin-right": 20, "margin-bottom": 20}
    )

