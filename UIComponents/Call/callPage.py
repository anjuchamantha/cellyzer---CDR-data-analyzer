import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import dash

from Call.callNavBar import CallNavBar


def CallPage():
    navbar = CallNavBar()
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
            form,
        ],
        style={"margin": 20, "margin-top": 100, }

    )

    # @CallPage.callback(
    #     dash.dependencies.Output('dd-output-container', 'children'),
    #     [dash.dependencies.Input('demo-dropdown', 'value')])
    # def update_output(value):
    #     return 'You have selected "{}"'.format(value)

    return html.Div(children=[content, navbar])
