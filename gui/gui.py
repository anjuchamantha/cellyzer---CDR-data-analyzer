import base64
import datetime
import io
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_admin_components as dac
import dash_bootstrap_components as dbc
import dash_table
import folium
import flask

import os
import sys

sys.path.insert(0, '../')

import cellyzer as cz

app = dash.Dash(__name__, external_stylesheets=[{dbc.themes.BOOTSTRAP}])
server = app.server

app.config.suppress_callback_exceptions = True

image_filename = 'cdr.jpg'
encoded_mage = base64.b64encode(open(image_filename, 'rb').read())

footer = dac.Footer(
    html.A("@Project CELLYZER",
           href="https://pypi.org/project/cellyzer/",
           target="_blank",
           ),
    right_text="2020"
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
    footer
])

indexrecorditems = [dac.SidebarButton(id='add-call-records',
                                      label='Add Call Record',
                                      icon='arrow-circle-right',
                                      href='/Call_Dataset'
                                      ),
                    dac.SidebarButton(id='add-msg-records',
                                      label='Add Message Record',
                                      icon='arrow-circle-right',
                                      href='/Message_Dataset'
                                      ),
                    dac.SidebarButton(id='add-cell-records',
                                      label='Add Cell Record',
                                      icon='arrow-circle-right',
                                      href='/Cell_Dataset'
                                      ),
                    ]
# Sidebar
indexpagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=indexrecorditems),
            dac.SidebarButton(id='tab_basic_boxes', label='Data Visualization', icon='desktop', href='page-4'),
            dac.SidebarButton(id='tab_value_boxes', label='Settings', icon='id-card', href='page-5')
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

## Front page
index_page = html.Div([
    html.H1(className='index_page_CELLYZER',
            children='CELLYZER'
            ),
    indexpagesidebar,
    html.Div([
        html.Div([
            html.Img(
                src='data:image/jpg;base64,{}'.format(encoded_mage.decode()),
                className='index_page_Img'
            ),
            html.Div([
                html.H1("WELCOME"),
                html.H1('CDR DATA ANALYSIS')
            ],
                className='index_page_welcome'
            )
        ],
            className='index_page_welcome_div')
    ])
],
    className='index_page_div'
)
# over front page

#######################################################################
## page for call dataset

callrecorditems = [dac.SidebarMenuItem(id='add-call-records',
                                       label='Add Call Record',
                                       icon='arrow-circle-right',
                                       children=[
                                           html.Div(id="call-data", style={"margin-left": "40px"})
                                       ]
                                       ),
                   ]

callpagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=callrecorditems)
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    url='/',
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

call_dataset = html.Div([
    html.H1(className='index_dataset_CELLYZER',
            children='CELLYZER'
            ),
    callpagesidebar,
    html.Div([
        html.H2("ADD CALL DATASET"),
        html.Hr(),
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Get File Path:", html_for="example-email-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath", placeholder="Enter path",
                            style={'width': '500px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H5(
                "Enter correct path of call dataset folder",
                style={'font-size': '17px', 'padding': '10px'}
            ),
            html.H5(
                "Do not enter file name to the path",
                style={'font-size': '17px', 'color': 'red', 'padding': '10px'}
            ),
            dbc.FormGroup(
                [
                    dbc.Label("File Type", html_for="example-radios-row", width=2),
                    dbc.Col(
                        dbc.RadioItems(
                            id="file-types-col",
                            options=[
                                {"label": "csv", "value": 1},
                                {"label": "excel", "value": 2},
                                {
                                    "label": "json",
                                    "value": 3,
                                },
                            ],
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
        ],
            style={
                'padding-left': '30px'
            }),
        html.Hr(),
        dcc.Upload(id='upload-data_call',
                   children=html.Div([
                       dbc.Button('ADD CALL DATA', className='index_datatset_calldata_button', color='dark'
                                  )
                   ]),
                   className='index_dataset_upload_data',
                   # Allow multiple files to be uploaded
                   multiple=True
                   ),
    ], className='call_page_welcome_div'),
],
    className='call_dataset_div'
)

calldatasetitems = [dac.SidebarMenuItem(id='add-call-records',
                                        label='Add Call Record',
                                        icon='arrow-circle-right'
                                        ),
                    ]

calldatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=calldatasetitems)
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    url='/',
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

call_dataset_file = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    calldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        dcc.Link('◙ Show All Data', href='/Call_Dataset/view_data'),
        html.Br(),
        dcc.Link('◙ Show All Users', href='/Call_Dataset/all_users'),
        html.Br(),
        dcc.Link('◙ Show Connected Users', href='/Call_Dataset/connected_users'),
        html.Br(),
        dcc.Link('◙ Call Records Between Two Selected Users', href='/Call_Dataset/records_between_users'),
        html.Br(),
        dcc.Link('◙ Close Contacts Of Selected Users', href='/Call_Dataset/close_contacts'),
        html.Br(),
        dcc.Link('◙ Ignored Call Details Of a User', href='/Call_Dataset/ignored_call'),
        html.Br(),
        dcc.Link('◙ Active Time Of a User', href='/Call_Dataset/active_time'),
        html.Br(),
        dcc.Link('◙ Visualize Connections Between All Users', href='/Call_Dataset/visualize_connection'),

    ], className='sample_call_data_visualize_option'),
],
    className='sample_call_dataset_div')

############ page for view all call data

viewcalldatasetitems = [dac.SidebarMenuItem(id='add-call-records',
                                            label='Add Call Record',
                                            icon='arrow-circle-right',
                                            children=html.Div([
                                                dcc.Link('◙ Show All Data', href='/Call_Dataset/view_data'),
                                                html.Br(),
                                                dcc.Link('◙ Show All Users', href='/Call_Dataset/all_users'),
                                                html.Br(),
                                                dcc.Link('◙ Show Connected Users',
                                                         href='/Call_Dataset/connected_users'),
                                                html.Br(),
                                                dcc.Link('◙ Call Records Between'
                                                         'Two Selected Users',
                                                         href='/Call_Dataset/records_between_users'),
                                                html.Br(),
                                                dcc.Link('◙ Close Contacts Of Selected Users',
                                                         href='/Call_Dataset/close_contacts'),
                                                html.Br(),
                                                dcc.Link('◙ Ignored Call Details Of a User',
                                                         href='/Call_Dataset/ignored_call'),
                                                html.Br(),
                                                dcc.Link('◙ Active Time Of a User', href='/Call_Dataset/active_time'),
                                                html.Br(),
                                                dcc.Link('◙ Visualize Connections Between All Users',
                                                         href='/Call_Dataset/visualize_connection'),
                                            ], style={'font-size': '12px', 'margin-left': '10px'})),
                        ]

viewcalldatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=viewcalldatasetitems)
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    url='/',
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

view_all_call_data = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - GET ALL DATA', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div([
        dbc.Button('VIEW DATA', outline=True, id='view', color='success', className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', outline=True, id='close', color='danger', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_data', className='sample_call_dataset_show'),
],
    className='sample_call_dataset_div')

######## page for get all users
get_all_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - GET ALL USERS', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize')
    ]),
    html.Div([
        dbc.Button('Get All Users', outline=True, color='success', id='get_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_all_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

####### page for show connected users of specific user
connected_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - SHOW CONNECTED USERS', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Specific User Number:", html_for="example-email"),
                dbc.Input(type="text", id="search", placeholder="Enter number", style={'width':'500px'}),
                dbc.FormText(
                    "Input must be a 10 digit number",
                    color="danger",
                ),
            ]
        ),
        dbc.Button('Connected Users', outline=True, color='success', id='connected_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_connected_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get call rercords between 2 users
records_between_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Call Records Between Users")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Call Records Between Two Users', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Two Numbers:'),
        dcc.Input(id="search_2", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        dcc.Input(id="search_3", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Get Records', id='record_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_records_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get close contacts
close_contacts = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Close Contacts")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Close Contacts Of a Selected User', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Number:'),
        dcc.Input(id="user_3", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.H6('Enter No. Top Contact:'),
        dcc.Input(id="contact", type='number', placeholder='Enter number of top contact'),
        html.Br(),
        html.Br(),
        html.Button('Close Contacts', id='close_contacts', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_close_contact', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### get ignored call details of a selected user
ignore_call_detail = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Ignored Call Details")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Ignored Call Details Of a Selected User', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Number:'),
        dcc.Input(id="user_5", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Ignored Call', id='ignore_call', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_ignore_call', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### get most active time of a user
active_time_user = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Active Time Of a User")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Active Time Of a Selected User', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter User:'),
        dcc.Input(id="user_4", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Active Time', id='active_time', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_active_time', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### visualize connections between all users
visualize_connections = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Visualize Connection")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Visualize Connections Between All Users', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('Visualize Connection', id='visualize_connection', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_visualize_connection', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

# over call dataset

call_data_list = []


@app.callback(Output('call-data', 'children'),
              [
                  Input('upload-data_call', 'filename'),
                  Input('filepath', 'value')
              ])
def add_call_dataset(filename, filepath):
    try:
        filename = filename[0]
        path_File = os.path.join(filepath, filename)
        call_data_list.append([filename, path_File])
        output_call = []
        for x in call_data_list:
            a = x[0].split('.')
            output_call.append(dcc.Link(a[0], href='/Call_Dataset/sample_call'))
            output_call.append(html.Br())
            # output_call.append(dcc.Link(a[0], href='/Call_Dataset/'+str(a[0]), id='link'))
        name = html.Div(children=output_call)
        return name

    except Exception as e:
        print(e)


######### view call dataset
@app.callback(Output('show_data', 'children'),
              [Input('view', 'n_clicks'), Input('close', 'n_clicks')
               ])
def update_table(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        dict_list = []
        for record in call_data.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab = []
        column = []
        for i in header:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        count = 0
        for j in dict_list:
            value = list(j.values())
            count += 1
            row_content = []
            if count > 100:
                break
            row_content = []
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.H2(filename),
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


############# set button value
@app.callback(Output('close', 'n_clicks'),
              [Input('view', 'n_clicks')
               ])
def close_data(n_clicks):
    if n_clicks is not None:
        return None


########## show all users
@app.callback(Output('show_all_users', 'children'),
              [Input('get_users', 'n_clicks')
               ])
def show_all_users(n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        all_users = call_data.get_all_users()
        tab = []
        column = []
        column.append(
            html.Th('Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for user in all_users:
            row_content = []
            row_content.append(html.Td(user, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '200px'
                              })
        ])
        return table


######## show cnnected users of specific user
@app.callback(Output('show_connected_users', 'children'),
              [Input('connected_users', 'n_clicks'),
               Input('search', 'value')
               ])
def show_connected_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        connected_users = call_data.get_connected_users(searchUser)
        tab = []
        column = []
        column.append(html.Th('Connected Users',
                              style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for user in connected_users:
            row_content = []
            row_content.append(html.Td(user, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '200px'
                              })
        ])
        return table


####### show records between 2 input users
@app.callback(Output('show_records_users', 'children'),
              [Input('search_3', 'value'),
               Input('search_2', 'value'),
               Input('record_users', 'n_clicks')
               ])
def between_users_records(user_1, user_2, click):
    table = html.Div()

    if click is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        dict_list = []
        for record in call_data.get_records(user_1, user_2):
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab = []
        column = []
        for i in header:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        count = 0
        for j in dict_list:
            value = list(j.values())
            count += 1
            row_content = []
            if count > 100:
                break
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


######## show close contacts
@app.callback(Output('show_close_contact', 'children'),
              [Input('user_3', 'value'),
               Input('contact', 'value'),
               Input('close_contacts', 'n_clicks')
               ])
def show_close_contatcs(user_3, contact, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        connected_users = call_data.get_close_contacts(user_3, contact)
        tab = []
        column = []
        col1 = html.Th("Contact No.",
                       style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col1)
        col2 = html.Th("No of interactions between users",
                       style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        numbers = list(connected_users.keys())
        NoContacts = list(connected_users.values())
        for j in range(len(numbers)):
            row_content = []
            row_content.append(html.Td(numbers[j], style={'border': '1px solid black', 'padding-left': '10px'}))
            row_content.append(html.Td(str(NoContacts[j]), style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '50%'
                              })
        ])
        return table


######## show most active time
@app.callback(Output('show_active_time', 'figure'),
              [Input('active_time', 'n_clicks'),
               Input('user_4', 'value')
               ])
def show_active_time(n_clicks, user_4):
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        active_time = call_data.get_most_active_time(user_4)
        return cz.visualization.active_time_bar_chart(active_time)


######### Show ignored call
@app.callback(Output('show_ignore_call', 'children'),
              [Input('user_5', 'value'),
               Input('ignore_call', 'n_clicks')
               ])
def show_ignore_call(user_5, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        ignore_call = call_data.get_ignored_call_details(user_5)
        key = list(ignore_call[0].keys())
        tab = []
        column = []
        for i in key:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for j in ignore_call:
            value = list(j.values())
            row_content = []
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


###### Visualize connection betwwen all users
@app.callback(Output('show_visualize_connection', 'children'),
              [Input('visualize_connection', 'n_clicks')
               ])
def show_visualize_connection(n_clicks):
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        filename = call_data_list[0][0]
        split_name = filename.split('.')
        file_type = split_name[-1]
        call_data = cz.read_call(filepath, file_type)
        visu_conn = call_data.visualize_connection_network()
        tab = []
        column = []
        col1 = html.Th("User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col1)
        col2 = html.Th("Connected User",
                       style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        for connection in visu_conn[0]:
            row_content = []
            row_content.append(html.Td(connection[0], style={'border': '1px solid black', 'padding-left': '10px'}))
            row_content.append(html.Td(connection[1], style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '50%'
                              })
        ])
        return table


###################################################################################################
###################################################################################################
## Page for cell dataset

cellrecorditems = [dac.SidebarMenuItem(id='add-cell-records',
                                       label='Add Cell Record',
                                       icon='arrow-circle-right',
                                       children=[
                                           html.Div(id="cell-data", style={"margin-left": "40px"})
                                       ]
                                       ),
                   ]

cellpagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=cellrecorditems)
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    url='/',
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

cell_dataset = html.Div([
    html.H1(className='index_cell_dataset_cellyzer', children='CELLYZER'),
    cellpagesidebar,
    html.Div([
        html.H2("ADD CELL DATASET"),
        html.Hr(),
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Get File Path:", html_for="example-email-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath_cell", placeholder="Enter path",
                            style={'width': '500px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H5(
                "Enter correct path of cell dataset folder",
                style={'font-size': '17px', 'padding': '10px'}
            ),
            html.H5(
                "Do not enter file name to the path",
                style={'font-size': '17px', 'color': 'red', 'padding': '10px'}
            ),
            dbc.FormGroup(
                [
                    dbc.Label("File Type", html_for="example-radios-row", width=2),
                    dbc.Col(
                        dbc.RadioItems(
                            id="file-types-col",
                            options=[
                                {"label": "csv", "value": 1},
                                {"label": "excel", "value": 2},
                                {
                                    "label": "json",
                                    "value": 3,
                                },
                            ],
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
        ],
            style={
                'padding-left': '30px'
            }),
        html.Hr(),
        dcc.Upload(id='upload-data_cell',
                   children=html.Div([
                       html.Button('ADD CELL DATA', className='index_celldata_add_button'
                                   )
                   ]),
                   className='index_cell_dataset_upload_data',
                   # Allow multiple files to be uploaded
                   multiple=True
                   ),
    ], className='call_page_welcome_div'),

],
    className='call_dataset_div'
)

cell_dataset_file = html.Div([
    html.H1(className='sample_cell_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_cell_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Cell Dataset")], className='index_dataset_Call_Dataset')
    ],
        className='sample_cell_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        dcc.Link('◙ Show All Data', href='/Cell_Dataset/view_cell_data'),
        html.Br(),
        dcc.Link('◙ Records Of a Specific Cell', href='/Cell_Dataset/records_cell_id'),
        html.Br(),
        dcc.Link('◙ Population Around Cell', href='/Cell_Dataset/population_around_cell'),
        html.Br(),
        dcc.Link('◙ Trip Visualization', href='/Cell_Dataset/trip_visualize'),
        html.Br(),
    ], className='sample_call_data_visualize_option'),
],
    className='sample_cell_dataset_div')

####### show all cell data
view_all_cell_data = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Cell Dataset")], className='index_dataset_Call_Dataset'),
        html.Div([html.H6("All Data")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Get All Data', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('VIEW DATA', id='view_cell', className='sample_call_dataset_viewdata'),
        html.Button('CLOSED DATA', id='close_cell', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_cell_data', className='sample_call_dataset_show'),
],
    className='sample_call_dataset_div')

###### get records of specific cell
records_of_cell = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Cell Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Records Cell")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H3(children='Records Of a Specific Cell', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Cell Id:'),
        dcc.Input(id="cell_id", type='number', placeholder='Enter Id'),
        html.Br(),
        html.Br(),
        html.Button('Records Cell', id='records_cell', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_records_cell', className='ndex_dataset_cell_record_div'),
],
    className='sample_call_dataset_div')

######## page for get ppulation and visualize
population_around_cell = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Cell Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Population Around Cell")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H3(children='Population Around Cell And Visualize', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('Get Population', id='population_button', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_population', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

######## page for trip visualization
trip_visualize = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Cell Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Trip Visualize")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H3(children='Trip Visualization', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter user number:'),
        dcc.Input(id="trip_user", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Trip Visualize', id='trip_visualize_button', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_trip_visualize', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

cell_data_list = []


####### add cell data
@app.callback(Output('cell-data', 'children'),
              [
                  Input('upload-data_cell', 'filename'),
                  Input('filepath_cell', 'value')
              ])
def add_cell_dataset(filename, filepath):
    try:
        filename = filename[0]
        path_File = os.path.join(filepath, filename)
        cell_data_list.append([filename, path_File])
        output_cell = []
        for x in cell_data_list:
            a = x[0].split('.')
            output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/sample_cell'))
            output_cell.append(html.Br())
        name_cell = html.Div(
            children=output_cell
        )
        return name_cell

    except Exception as e:
        print(e)


@app.callback(Output('show_cell_data', 'children'),
              [Input('view_cell', 'n_clicks'), Input('close_cell', 'n_clicks')
               ])
def view_cell_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        filename_call = call_data_list[0][0]
        split_call_name = filename_call.split('.')
        file_type_call = split_call_name[-1]
        call_data = cz.read_call(filepath_call, file_type_call)
        split_name = filename.split('.')
        file_type = split_name[-1]
        c = cz.read_cell(filepath, filepath_call, call_data, file_type)
        dict_list = []
        for record in c.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab = []
        column = []
        for i in header:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        count = 0
        for j in dict_list:
            value = list(j.values())
            count += 1
            row_content = []
            if count > 100:
                break
            row_content = []
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.H2(filename),
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


@app.callback(Output('close_cell', 'n_clicks'),
              [Input('view_cell', 'n_clicks')
               ])
def close_cell_data(n_clicks):
    if n_clicks is not None:
        return None


###### get cell_id records
@app.callback(Output('show_records_cell', 'children'),
              [Input('records_cell', 'n_clicks'),
               Input('cell_id', 'value')
               ])
def get_cell_records(n_clicks, cell_id):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        filename_call = call_data_list[0][0]
        split_call_name = filename_call.split('.')
        file_type_call = split_call_name[-1]
        call_data = cz.read_call(filepath_call, file_type_call)
        split_name = filename.split('.')
        file_type = split_name[-1]
        antana_dataset = cz.read_cell(filepath, filepath_call, call_data, file_type)
        record_cell = antana_dataset.get_cell_records(cell_id)
        cell = record_cell.get_cell_id()
        print(record_cell)
        return html.H5('Cell_id: ' + cell, className='index_dataset_add_call_data')


######## get population around cell
@app.callback(Output('show_population', 'children'),
              [Input('population_button', 'n_clicks'),
               ])
def get_population(n_clicks):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        filename_call = call_data_list[0][0]
        split_call_name = filename_call.split('.')
        file_type_call = split_call_name[-1]
        call_data = cz.read_call(filepath_call, file_type_call)
        split_name = filename.split('.')
        file_type = split_name[-1]
        antana_dataset = cz.read_cell(filepath, filepath_call, call_data, file_type)
        population = antana_dataset.get_population()
        return cz.visualization.cell_population_visualization(population)


######### get trip visualize
@app.callback(Output('show_trip_visualize', 'children'),
              [Input('trip_user', 'value'),
               Input('trip_visualize_button', 'n_clicks')
               ])
def trip_visualization(user, n_clicks):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        filename_call = call_data_list[0][0]
        split_call_name = filename_call.split('.')
        file_type_call = split_call_name[-1]
        call_data = cz.read_call(filepath_call, file_type_call)
        split_name = filename.split('.')
        file_type = split_name[-1]
        antana_dataset = cz.read_cell(filepath, filepath_call, call_data, file_type)
        trip_visualize = antana_dataset.get_trip_details(user)

        return cz.visualization.trip_visualization(trip_visualize)


# over cell
###########################################################################
###########################################################################
## Page for message dataset

messagerecorditems = [dac.SidebarMenuItem(id='add-message-records',
                                          label='Add Message Record',
                                          icon='arrow-circle-right',
                                          children=[
                                              html.Div(id="message-data", style={"margin-left": "40px"})
                                          ]
                                          ),
                      ]

messagepagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=messagerecorditems)
        ]
    ),
    title='DASHBOARD',
    color="primary",
    brand_color="secondary",
    url='/',
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

message_dataset = html.Div([
    html.H1(className='index_message_dataset_cellyzer',
            children='CELLYZER'
            ),
    messagepagesidebar,
    html.Div([
        html.H2("ADD MESSAGE DATASET"),
        html.Hr(),
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Get File Path:", html_for="example-email-row", width=2),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath_message", placeholder="Enter path",
                            style={'width': '500px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H5(
                "Enter correct path of cell dataset folder",
                style={'font-size': '17px', 'padding': '10px'}
            ),
            html.H5(
                "Do not enter file name to the path",
                style={'font-size': '17px', 'color': 'red', 'padding': '10px'}
            ),
            dbc.FormGroup(
                [
                    dbc.Label("File Type", html_for="example-radios-row", width=2),
                    dbc.Col(
                        dbc.RadioItems(
                            id="file-types-col",
                            options=[
                                {"label": "csv", "value": 1},
                                {"label": "excel", "value": 2},
                                {
                                    "label": "json",
                                    "value": 3,
                                },
                            ],
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
        ],
            style={
                'padding-left': '30px'
            }),
        html.Hr(),
        dcc.Upload(id='upload-data_message',
                   children=html.Div([
                       html.Button('ADD MESSAGE DATA', className='index_messagedata_add_button'
                                   )
                   ]),
                   className='index_message_dataset_upload_data',
                   # Allow multiple files to be uploaded
                   multiple=True
                   ),
    ], className='call_page_welcome_div'),
],
    className='call_dataset_div'
)

message_data_file = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_dataset_Call_Dataset'),
    ],
        className='sample_dataset_Dashboard_div'),
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        dcc.Link('◙ Show All Message Data', href='/Message_Dataset/view_data'),
        html.Br(),
        dcc.Link('◙ Show All Users', href='/Message_Dataset/all_users'),
        html.Br(),
        dcc.Link('◙ Show Connected Users', href='/Message_Dataset/connected_users'),
        html.Br(),
        dcc.Link('◙ Call Records Between Two Selected Users', href='/Message_Dataset/records_between_users'),
        html.Br(),
        dcc.Link('◙ Visualize Connections Between All Users', href='/Message_Dataset/visualize_connection'),

    ], className='sample_call_data_visualize_option'),
],
    className='sample_call_dataset_div')

############ page for view all message data
view_all_message_data = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_dataset_Call_Dataset'),
        html.Div([html.H6("All Data")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Get All Data', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('VIEW DATA', id='view_message', className='sample_call_dataset_viewdata'),
        html.Button('CLOSED DATA', id='close_message', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_message_data', className='sample_call_dataset_show'),
],
    className='sample_call_dataset_div')

######## page for get all users in message dataset
get_all_message_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("All Users")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div')
    ]),
    html.Div([
        html.H4(children='Get All Users', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('Get All Users', id='get_message_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_all_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

####### page for show connected users of specific user im message dataset
connected_message_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Connected Users")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H4('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H3(children='Connected Users Of Specific Message User', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Specific User Number:'),
        dcc.Input(id="user_message", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Connected Users', id='connected_message_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_connected_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get call rercords between 2 users
message_records_between_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Message Records Between Users")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Message Records Between Two Users', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.H6('Enter Two Numbers:'),
        dcc.Input(id="message_user2", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        dcc.Input(id="message_user3", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Get Records', id='record_message_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_records_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### visualize connections between all users
visualize_message_connections = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'),
        html.Div([html.H5("Message Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("Visualize Connection")], className='index_page_dataset_div_all_user')
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='index_dataset_add_call_data_div'),
    ]),
    html.Div([
        html.H4(children='Visualize Connections Between All Users', className='sample_call_visualize_all_user')],
        style={'padding-left': '30px', 'margin-top': '40px', 'margin-bottom': '20px'}
    ),
    html.Div([
        html.Button('Visualize Connection', id='visualize_message_connection',
                    className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_visualize_message_connection', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

message_data_list = []


######## add message dataset
@app.callback(Output('message-data', 'children'),
              [
                  Input('upload-data_message', 'filename'),
                  Input('filepath_message', 'value')
              ])
def add_message_dataset(filename, filepath):
    try:
        filename = filename[0]
        path_File = os.path.join(filepath, filename)
        message_data_list.append([filename, path_File])
        output_message = []
        for x in message_data_list:
            a = x[0].split('.')
            output_message.append(dcc.Link(a[0], href='/Message_Dataset/sample_message'))
            output_message.append(html.Br())
        name_message = html.Div(
            children=output_message
        )
        return name_message

    except Exception as e:
        print(e)


####### view all message data
@app.callback(Output('show_message_data', 'children'),
              [Input('view_message', 'n_clicks'), Input('close_message', 'n_clicks')
               ])
def view_message_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name = filename_message.split('.')
        file_type = split_name[-1]
        message_data = cz.read_msg(filepath_message, file_type)
        dict_list = []
        for record in message_data.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab = []
        column = []
        for i in header:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        count = 0
        for j in dict_list:
            value = list(j.values())
            count += 1
            row_content = []
            if count > 100:
                break
            row_content = []
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.H2(filename_message),
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


########## set button value
@app.callback(Output('close_message', 'n_clicks'),
              [Input('view_message', 'n_clicks')
               ])
def close_message_data(n_clicks):
    if n_clicks is not None:
        return None


########## show all message users
@app.callback(Output('show_all_message_users', 'children'),
              [Input('get_message_users', 'n_clicks')
               ])
def show_all_message_users(n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name = filename_message.split('.')
        file_type = split_name[-1]
        message_data = cz.read_msg(filepath_message, file_type)
        all_users = message_data.get_all_users()
        tab = []
        column = []
        column.append(
            html.Th('Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for user in all_users:
            row_content = []
            row_content.append(html.Td(user, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '200px'
                              })
        ])
        return table


######## show cnnected users of specific user in message dataset
@app.callback(Output('show_connected_message_users', 'children'),
              [Input('connected_message_users', 'n_clicks'),
               Input('user_message', 'value')
               ])
def show_connected_message_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name = filename_message.split('.')
        file_type = split_name[-1]
        message_data = cz.read_msg(filepath_message, file_type)
        connected_users = message_data.get_connected_users(searchUser)
        tab = []
        column = []
        column.append(html.Th('Connected Users',
                              style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for user in connected_users:
            row_content = []
            row_content.append(html.Td(user, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '200px'
                              })
        ])
        return table


####### show message records between 2 input users
@app.callback(Output('show_records_message_users', 'children'),
              [Input('message_user3', 'value'),
               Input('message_user2', 'value'),
               Input('record_message_users', 'n_clicks')
               ])
def between_message_users_records(user_1, user_2, click):
    table = html.Div()

    if click is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name = filename_message.split('.')
        file_type = split_name[-1]
        message_data = cz.read_msg(filepath_message, file_type)
        dict_list = []
        for record in message_data.get_records(user_1, user_2):
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab = []
        column = []
        for i in header:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        count = 0
        for j in dict_list:
            value = list(j.values())
            count += 1
            row_content = []
            if count > 100:
                break
            for x in value:
                row_content.append(html.Td(x, style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '100%'
                              })
        ])
        return table


###### Visualize connection betwwen all users in message dataset
@app.callback(Output('show_visualize_message_connection', 'children'),
              [Input('visualize_message_connection', 'n_clicks')
               ])
def show_visualize_message_connection(n_clicks):
    table = html.Div()

    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name = filename_message.split('.')
        file_type = split_name[-1]
        message_data = cz.read_msg(filepath_message, file_type)
        visu_conn = message_data.visualize_connection_network()
        tab = []
        column = []
        col1 = html.Th("User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col1)
        col2 = html.Th("Connected User",
                       style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        for connection in visu_conn[0]:
            row_content = []
            row_content.append(html.Td(connection[0], style={'border': '1px solid black', 'padding-left': '10px'}))
            row_content.append(html.Td(connection[1], style={'border': '1px solid black', 'padding-left': '10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table = html.Div([
            html.Table(children=tab,
                       style={'border-collapse': 'collapse',
                              'border': '1px solid black',
                              'width': '50%'
                              })
        ])
        return table


# over message dataset


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')
               ])
def display_page(pathname):
    if pathname == '/Call_Dataset':
        return call_dataset
    elif pathname == '/Cell_Dataset':
        return cell_dataset
    elif pathname == '/Message_Dataset':
        return message_dataset
    elif pathname == '/Call_Dataset/view_data':
        return view_all_call_data
    elif pathname == '/Call_Dataset/all_users':
        return get_all_users
    elif pathname == '/Call_Dataset/connected_users':
        return connected_users
    elif pathname == '/Call_Dataset/records_between_users':
        return records_between_users
    elif pathname == '/Call_Dataset/close_contacts':
        return close_contacts
    elif pathname == '/Call_Dataset/ignored_call':
        return ignore_call_detail
    elif pathname == '/Call_Dataset/active_time':
        return active_time_user
    elif pathname == '/Call_Dataset/visualize_connection':
        return visualize_connections
    elif pathname == '/Call_Dataset/sample_call':
        return call_dataset_file
    elif pathname == '/Cell_Dataset/sample_cell':
        return cell_dataset_file
    elif pathname == '/Cell_Dataset/view_cell_data':
        return view_all_cell_data
    elif pathname == "/Cell_Dataset/records_cell_id":
        return records_of_cell
    elif pathname == '/Cell_Dataset/population_around_cell':
        return population_around_cell
    elif pathname == '/Cell_Dataset/trip_visualize':
        return trip_visualize
    elif pathname == '/Message_Dataset/sample_message':
        return message_data_file
    elif pathname == '/Message_Dataset/view_data':
        return view_all_message_data
    elif pathname == '/Message_Dataset/all_users':
        return get_all_message_users
    elif pathname == '/Message_Dataset/connected_users':
        return connected_message_users
    elif pathname == '/Message_Dataset/records_between_users':
        return message_records_between_users
    elif pathname == '/Message_Dataset/visualize_connection':
        return visualize_message_connections
    elif pathname == '/':
        return index_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
