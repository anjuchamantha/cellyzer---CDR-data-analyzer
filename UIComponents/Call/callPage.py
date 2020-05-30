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
        style={"width": 300, "margin-right": 20, "margin-bottom": 50, }
    )


def CallPage(name="<Calls>"):
    navbar = SimpleTitleBar(name="Call Dataset : %s" % name)
    dataset_card = DataSetCard(name=name, records="1324")
    func_dropdown = dbc.FormGroup(
        [
            dbc.Label("Select Function", html_for="dropdown"),
            dcc.Dropdown(
                id="func_dropdown",
                options=[
                    {"label": "Option 1", "value": 1},
                    {"label": "Option 2", "value": 2},
                ],
            ),
        ],
        style={"margin-bottom": 20}
    )
    param_dropdown = dbc.FormGroup(
        [
            dbc.Label("Select Optional Parameters", html_for="dropdown"),
            dcc.Dropdown(
                id="param_dropdown",
                options=[
                    {"label": "User 1", "value": "user1"},
                    {"label": "User 2", "value": "user2"},
                ],
                multi=True
            ),
        ],
        style={"margin-bottom": 70}
    )

    email_input = dbc.FormGroup(
        [
            dbc.Label("User 1", width=2),
            dbc.Col(
                dbc.Input(
                    id="user1-input", placeholder="Enter phone number"
                ),
                width=10,
            ),
        ],
        row=True,
    )

    password_input = dbc.FormGroup(
        [
            dbc.Label("User 2", width=2),
            dbc.Col(
                dbc.Input(
                    id="user2-input",
                    placeholder="Enter phone number",
                ),
                width=10,
            ),
        ],
        row=True,
    )

    form = dbc.Form([func_dropdown, param_dropdown, email_input, password_input, ])

    content = html.Div(
        children=[
            dataset_card,
            form,
        ],
        style={"margin": 20, "margin-top": 100, }

    )

    return html.Div(children=[content, navbar])
