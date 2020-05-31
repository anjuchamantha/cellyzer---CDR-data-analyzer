import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

from simpleTitleBar import SimpleTitleBar


def DataSetCard(name, records="-", field_names=["user", "other_user"], ):
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
                    html.H5("7", style={"font-size": 50, "margin-bottom": 0}),
                    html.P(
                        "fields", style={}
                    ),
                ],
                style={"text-align": "center", "height": 250}
            ),
        ],
        style={"width": "30%", "margin-right": 20, "margin-bottom": 50, "height": 320}
    )


def MessagePage(name="<Message>"):
    navbar = SimpleTitleBar(name="Call Dataset : %s" % name)
    dataset_card = DataSetCard(name=name, records="1324")

    functionality_list = html.Div(
        [
            dbc.Row(dbc.Button("Show All Data", color="light", className="mr-1", block=True,
                               style={"margin-bottom": 10, "text-align": 'start'})),
            dbc.Row(dbc.Button("Show All the users", color="light", className="mr-1", block=True,
                               style={"margin-bottom": 10, "text-align": 'start'})),
            dbc.Row(dbc.Button("Show connected users", color="light", className="mr-1", block=True,
                               style={"margin-bottom": 10, "text-align": 'start'})),
            dbc.Row(dbc.Button("Message records between 2 selected users", color="light", className="mr-1", block=True,
                               style={"margin-bottom": 10, "text-align": 'start'})),
            dbc.Row(dbc.Button(["Visualize connections between all users ",
                                dbc.Badge("Heavy Function", color="danger", className="mr-1")],
                               color="light",
                               className="mr-1",
                               block=True,
                               style={"margin-bottom": 10, "text-align": 'start'}, )),
        ]
    )

    content = dbc.Row(
        children=[

            dbc.Card(
                children=[
                    dbc.CardHeader(html.H5("Available Functions", style={"text-align": "center"})),
                    dbc.CardBody(
                        functionality_list,
                        style={"text-align": "center"}
                    ),
                ],
                style={"margin-right": 20, "margin-bottom": 50, "width": "60%"}
            ),
            dataset_card,

        ],
        style={"margin": 20, "margin-top": 100, }

    )

    return html.Div(children=[content, navbar])
