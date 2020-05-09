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
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
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
        ],
            style={
                'padding-left': '30px'
            }),
        html.Hr(),
        dcc.Upload(id='upload-data_call',
                   children=html.Div([
                       dbc.Button('CHOOSE FILE', id='choose_call', className='index_datatset_calldata_button', color='dark'
                                  )
                   ]),
                   className='index_dataset_upload_data',
                   # Allow multiple files to be uploaded
                   multiple=True
                   ),
        html.Div([
            html.Button('ADD CALL DATA', id='adding_call' ,className='index_celldata_add_button',),
            ]),
        dbc.Alert(id='alert', dismissable=True, is_open=False, style={'width':'500px', 'background-color':'red','font-size':'18px'})
    ], className='call_page_welcome_div'),
],
    className='call_dataset_div'
)

calldatasetitems = [dac.SidebarMenuItem(id='add-call-records',
                                        label='Add Call Record',
                                        icon='arrow-circle-right',
                                        children=[
                                            html.Div(id="file_name", style={"margin-left": "40px", 'color': 'white'})
                                        ]
                                        ),
                    ]

calldatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
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
    html.Div(id='call_option', className='sample_call_data_visualize_option'),
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
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
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
    html.Hr(),
    html.Br(),
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
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('Get All Users', outline=True, color='success', id='get_users',
                   className='sample_call_dataset_viewdata')],
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
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Specific User Number:", html_for="example-email"),
                dbc.Input(type="text", id="search", placeholder="Enter number", style={'width': '500px'}),
                dbc.FormText(
                    "Input must be a 10 digit number",
                    color="danger",
                ),
            ]
        ),
        dbc.Button('Connected Users', outline=True, color='success', id='connected_users',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_connected_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get call rercords between 2 users
records_between_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - CALL RECORDS BETWEEN TWO USERS',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Div([
        html.H4('Enter Two Numbers:'),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("First Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="search_2", placeholder="Enter first number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.FormGroup(
            [
                dbc.Label("Second Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="search_3", placeholder="Enter second number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Get Records', id='record_users', color='success', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div',
    ),
    html.Div(id='show_records_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get close contacts
close_contacts = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - CLOSE CONTACTS OF A SELECTED USER',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize', style={'width': '1000px'}),
    ]),
    html.Hr(),
    html.Div([
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("Enter Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="user_3", placeholder="Enter number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.FormGroup(
            [
                dbc.Label("Enter No. Top Contact:", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="number", id="contact", placeholder="Enter number of top contact", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Close Contacts', id='close_contacts', color='success', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_close_contact', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### get ignored call details of a selected user
ignore_call_detail = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - IGNORED CALL DETAILS OF A SELECTED USER',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize', style={'width': '1100px'}),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="user_5", placeholder="Enter number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Ignored Call', id='ignore_call', color='success', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_ignore_call', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### get most active time of a user
active_time_user = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - ACTIVE TIME OF A SELECTED USER',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize', style={'width': '1000px'}),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter User", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="user_4", placeholder="Enter number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Active Time', id='active_time', color='success', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_active_time', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### visualize connections between all users
visualize_connections = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcalldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION - VISUALIZE CONNECTIONS', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('Visualize Connection', id='visualize_connection', color='danger', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_visualize_connection', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

# over call dataset

FilePath = []
call_data_list = []
update_call_data = []
call_option = []
call_name = []


###### add call data
@app.callback([ Output('call-data', 'children'), Output('alert', 'is_open'), Output('alert', 'children')],
              [ Input('upload-data_call', 'filename'), Input('filepath', 'value'), Input('adding_call', 'n_clicks')],
              [  State('alert', 'is_open')]
            )
def add_call_dataset(filename, filepath, n_clicks, is_open):
    if n_clicks is not None:
        try:
            FilePath.append(filepath)
            filename=filename[0]
            path_File=os.path.join(filepath, filename)
            file_part=filename.split('.')
            file_type = file_part[-1]
            call_data = cz.read_call(path_File, file_type)
            all_users = call_data.get_all_users()
            call_data_list.append([filename, path_File, all_users, call_data])
            call_name.append(file_part[0])
            option=[]
            option.append(dcc.Link('◙ Show All Data', href='/Call_Dataset/{}/view_data'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Show All Users', href='/Call_Dataset/{}/all_users'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Show Connected Users', href='/Call_Dataset/{}/connected_users'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Call Records Between Two Selected Users', href='/Call_Dataset/{}/records_between_users'.format(file_part[0]))) 
            option.append(html.Br()) 
            option.append(dcc.Link('◙ Close Contacts Of Selected Users', href='/Call_Dataset/{}/close_contacts'.format(file_part[0])))
            option.append(html.Br()) 
            option.append(dcc.Link('◙ Ignored Call Details Of a User', href='/Call_Dataset/{}/ignored_call'.format(file_part[0]))) 
            option.append(html.Br()) 
            option.append(dcc.Link('◙ Active Time Of a User', href='/Call_Dataset/{}/active_time'.format(file_part[0]))) 
            option.append(html.Br()) 
            option.append(dcc.Link('◙ Visualize Connections Between All Users', href='/Call_Dataset/{}/visualize_connection'.format(file_part[0]))) 
            call_option.append([file_part[0], option])
            output_call=[]
            for x in call_data_list:
                a=x[0].split('.')
                output_call.append(html.Br())
                output_call.append(dcc.Link(a[0], href='/Call_Dataset/'+str(a[0])))
            name=html.Div(children=output_call)
            return name, is_open, None

        except Exception as e:
            print(str(e))
            if str(e) == "'NoneType' object has no attribute 'get_all_users'":
                word = "File path is incorrect"
            else:
                word = "Dataset is not call dataset"
            output_call=[]
            for x in call_data_list:
                a=x[0].split('.')
                output_call.append(html.Br())
                output_call.append(dcc.Link(a[0], href='/Call_Dataset/'+str(a[0])))
            name=html.Div(children=output_call)
            return name, not is_open, word
        
    else:
        output_call=[]
        for x in call_data_list:
            a=x[0].split('.')
            output_call.append(html.Br())
            output_call.append(dcc.Link(a[0], href='/Call_Dataset/'+str(a[0])))
        name=html.Div(children=output_call)
        return name, False , None


@app.callback(Output('adding_call', 'n_clicks'),
              [Input('choose_call', 'n_clicks'), Input('filepath', 'value')])
def adding_call_button(n_clicks, filepath):
    if len(FilePath)>=1 and FilePath[-1]!=filepath:
        return None
    elif n_clicks is not None:
        return None

######## return file name to the next page
@app.callback( dash.dependencies.Output('file_name', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name(pathname): 
    file_call = pathname.split('/')
    for a in call_option:
        if file_call[-1] == a[0]:
            for data in call_data_list:
                dataNew= data[0].split('.')
                if file_call[-1]== dataNew[0]:
                    update_call_data.append(data)
                    
            return file_call[-1]


######## get call option
@app.callback(dash.dependencies.Output('call_option', 'children'),
              [dash.dependencies.Input('url', 'pathname')
               ])
def file_name2(pathname):
    file_call = pathname.split('/')
    for a in call_option:
        if file_call[-1] == a[0]:
            return a[1]

######### view call dataset
@app.callback(Output('show_data', 'children'),
              [ Input('view', 'n_clicks'),
                Input('close', 'n_clicks')
               ])
def update_table(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        call_data = update_call_data[-1][-1]
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
            # html.H2(filename),
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
        all_users = update_call_data[-1][2]
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


######## show connected users of specific user
@app.callback(Output('show_connected_users', 'children'),
              [Input('connected_users', 'n_clicks'),
               Input('search', 'value')
               ])
def show_connected_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        call_data = update_call_data[-1][-1]
        connected_users = call_data.get_connected_users(searchUser)   
        if len(connected_users)==0:
            table=html.Div([
                html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        else:
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
        call_data = update_call_data[-1][-1]
        call_users = update_call_data[-1][2]
        dict_list = []
        if user_1 not in call_users:
            table=html.Div([
                html.H5(children='User 2 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        elif user_2 not in call_users:
            table=html.Div([
                html.H5(children='User 1 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
        else:
            for record in call_data.get_records(user_1, user_2):
                dict_list.append(vars(record))
            header = list(dict_list[0].keys())              
            if len(dict_list)==0:
                table=html.Div([
                    html.H5(children='No records between two users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:                  
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
        call_data = update_call_data[-1][-1]
        call_users = update_call_data[-1][2]
        connected_users = call_data.get_close_contacts(user_3, contact)
        if user_3 not in call_users:
            table=html.Div([
                html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        else:
            connected_users = call_data.get_close_contacts(user_3, contact)
            if len(connected_users)==0:
                table=html.Div([
                    html.H5(children='No connected users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
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
@app.callback(Output('show_active_time', 'children'),
              [Input('active_time', 'n_clicks'),
               Input('user_4', 'value')
               ])
def show_active_time(n_clicks, user_4):
    table = html.Div()
    try:
        if n_clicks is not None:
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            if user_4 not in call_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])          
            else:
                active_time = call_data.get_most_active_time(user_4)
                cz.visualization.active_time_bar_chart(active_time)
            return table
    
    except Exception as e:
        print(e)
    

######### Show ignored call
@app.callback(Output('show_ignore_call', 'children'),
              [Input('user_5', 'value'),
               Input('ignore_call', 'n_clicks')
               ])
def show_ignore_call(user_5, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        call_data = update_call_data[-1][-1]
        call_users = update_call_data[-1][2]
        if user_5 not in call_users:
            table=html.Div([
                html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        else:
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
        call_data = update_call_data[-1][-1]
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
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
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
                "*Enter correct path of cell dataset folder and Do not enter file name to the path",
                style={'font-size': '13px', 'color': 'red', 'padding': '10px'},
            ),
        ],
            style={
                'padding-left': '30px'
            }),
        dcc.Upload(id='upload-data_cell',
                   children=html.Div([
                       dbc.Button('SELECT CELL DATA', outline=True, color='success')]),
                   className='index_cell_dataset_upload_data',
                   multiple=True),
        html.Hr(),
        html.Div([
            html.H5('*Please add call dataset before adding cell dataset', style={'font-size': '15px'}),
            html.Div([
                dbc.Button('SELECT CALL DATA', outline=True, color='success', id='call_for_cell'),
                dcc.Dropdown(id='select_call', style={'width': '200px', 'float': 'right', 'color': 'red'})
            ], style={'padding':'10px 0px'})
        ], style={'padding-right': '300px'}),
        html.Br(),
        html.Hr(),
        html.Div([
            dbc.Button('ADD DATA', outline=True, color='danger', id='show_cell_dash'),
        ])
    ], className='call_page_welcome_div'),

],
    className='call_dataset_div'
)

celldatasetitems = [dac.SidebarMenuItem(id='add-cell-records',
                                        label='Add Cell Record',
                                        icon='arrow-circle-right',
                                        children=[
                                            html.Div(id="file_name_cell",
                                                     style={"margin-left": "40px", 'color': 'white'})
                                        ]
                                        ),
                    ]

celldatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=celldatasetitems)
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

cell_dataset_file = html.Div([
    html.H1(className='sample_cell_data_cellyzer', children='CELLYZER'),
    celldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div(id='cell_option', className='sample_call_data_visualize_option'),
],
    className='sample_cell_dataset_div')

####### show all cell data

viewcelldatasetitems = [dac.SidebarMenuItem(id='add-cell-records',
                                            label='Add Cell Record',
                                            icon='arrow-circle-right',
                                            children=html.Div([
                                                dcc.Link('◙ Show All Data', href='/Cell_Dataset/view_cell_data'),
                                                html.Br(),
                                                dcc.Link('◙ Records Of a Specific Cell',
                                                         href='/Cell_Dataset/records_cell_id'),
                                                html.Br(),
                                                dcc.Link('◙ Population Around Cell',
                                                         href='/Cell_Dataset/population_around_cell'),
                                                html.Br(),
                                                dcc.Link('◙ Trip Visualization', href='/Cell_Dataset/trip_visualize'),
                                                html.Br(),
                                            ], style={'font-size': '12px', 'margin-left': '10px'})),
                        ]

viewcelldatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=viewcelldatasetitems)
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

view_all_cell_data = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcelldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION - GET ALL DATA', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('VIEW DATA', id='view_cell', outline=True, color='success',
                   className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', id='close_cell', outline=True, color='danger',
                   className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_cell_data', className='sample_call_dataset_show'),
],
    className='sample_call_dataset_div')

###### get records of specific cell
records_of_cell = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcelldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION - RECORDS OF A SPECIFIC CELL',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Cell ID", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="number", id="cell_id", placeholder="Enter ID", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Records Cell', id='records_cell', outline=True, color='success',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_records_cell', className='ndex_dataset_cell_record_div'),
],
    className='sample_call_dataset_div')

######## page for get population and visualize
population_around_cell = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcelldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION - POPULATION AROUND CELL AND VISUALIZE',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize', style={'width': '1000px'}),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('Get Population', id='population_button', outline=True, color='danger',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_population', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

######## page for trip visualization
trip_visualize = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewcelldatasetidebar,
    html.Div([
        html.Div([
            html.H3('CELL  DATASET  VISUALIZATION - TRIP VISAULIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter user number:", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="trip_user", placeholder="Enter number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Trip Visualize', id='trip_visualize_button', outline=True, color='danger',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_trip_visualize', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

cell_data_list = []
update_cell_data = []
cell_option = []


####### add cell data
@app.callback(Output('cell-data', 'children'),

            [   Input('select_call', 'value'),
                Input('upload-data_cell', 'filename'),
                Input('filepath_cell', 'value'),
                Input('show_cell_dash', 'n_clicks')
            ])
def add_cell_dataset(call_file, filename, filepath, n_clicks):
    try:
        if n_clicks is not None:
            filename=filename[0]
            path_File=os.path.join(filepath, filename)
            file_part=filename.split('.')
            file_type = file_part[-1]
            for call in call_data_list:
                f_name= call[0].split('.')
                if call_file == f_name[0]:
                    cell_data = cz.read_cell(path_File, call[1], call[-1], file_type)
                    cell_data_list.append([filename, path_File, call[2], cell_data])
                    break
            option=[]
            option.append(dcc.Link('◙ Show All Data', href='/Cell_Dataset/{}/view_cell_data'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Records Of a Specific Cell', href='/Cell_Dataset/{}/records_cell_id'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Population Around Cell', href='/Cell_Dataset/{}/population_around_cell'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Trip Visualization', href='/Cell_Dataset/{}/trip_visualize'.format(file_part[0]))) 
            cell_option.append([file_part[0], option])
            output_cell=[]
            for x in cell_data_list:
                a=x[0].split('.')
                output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/'+str(a[0])))
                output_cell.append(html.Br())
            name_cell=html.Div(children = output_cell)
            return name_cell

    except Exception as e:
        print(e)
        output_cell=[]
        for x in cell_data_list:
            a=x[0].split('.')
            output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/'+str(a[0])))
            output_cell.append(html.Br())
        name_cell=html.Div(children = output_cell)
        return name_cell


########### show cell data
@app.callback(Output('show_cell_data', 'children'),
              [ Input('view_cell', 'n_clicks'), 
                Input('close_cell', 'n_clicks')
               ])
def view_cell_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        cell_data = update_cell_data[-1][-1]
        dict_list = []
        for record in cell_data.get_records():
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
            # html.H2(filename),
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

######## select call dataset using dropdown
@app.callback(Output('select_call', 'options'),
            [   Input('call_for_cell', 'n_clicks')
            ])
def get_call_for_cell(n_clicks):
    if n_clicks is not None:
        add_call=[]
        for name in call_name:
            add_call.append({'label':name, 'value': name})
        return add_call

###### get cell_id records
@app.callback(Output('show_records_cell', 'children'),
              [Input('records_cell', 'n_clicks'),
               Input('cell_id', 'value')
               ])
def get_cell_records(n_clicks, cell_id):
    if n_clicks is not None:
        try:
            antana_dataset = update_cell_data[-1][-1]
            record_cell = antana_dataset.get_cell_records(cell_id)
            cell = record_cell.get_cell_id()
        
        except Exception as e:
            print(e)
            cell="Id does not exist"
        return html.H5('Cell_id: ' + cell, className='index_dataset_add_call_data')


######## get population around cell
@app.callback(Output('show_population', 'children'),
              [Input('population_button', 'n_clicks'),
               ])
def get_population(n_clicks):
    if n_clicks is not None:
        antana_dataset = update_cell_data[-1][-1]
        population = antana_dataset.get_population()
        return cz.visualization.cell_population_visualization(population)


######### get trip visualize
@app.callback(Output('show_trip_visualize', 'children'),
              [Input('trip_user', 'value'),
               Input('trip_visualize_button', 'n_clicks')
               ])
def trip_visualization(user, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        all_users= update_cell_data[-1][2]
        if user not in all_users:
            table=html.Div([
                html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        else:
            antana_dataset = update_cell_data[-1][-1]
            trip_visualize = antana_dataset.get_trip_details(user)
            cz.visualization.trip_visualization(trip_visualize)
        return table

######## return cell file name to the next page
@app.callback( dash.dependencies.Output('file_name_cell', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name_cell(pathname): 
    file_cell = pathname.split('/')
    for a in cell_option:
        if file_cell[-1] == a[0]:
            for data in cell_data_list:
                dataNew= data[0].split('.')
                if file_cell[-1]== dataNew[0]:
                    update_cell_data.append(data)
                    
            return file_cell[-1]

######## get cell option
@app.callback( dash.dependencies.Output('cell_option', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def cell_option_visu(pathname): 
    file_cell = pathname.split('/')
    for a in cell_option:
        if file_cell[-1] == a[0]:
            return a[1]

# over cell
################################################################################################
################################################################################################
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
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
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
            # dbc.FormGroup(
            #     [
            #         dbc.Label("File Type", html_for="example-radios-row", width=2),
            #         dbc.Col(
            #             dbc.RadioItems(
            #                 id="file-types-col",
            #                 options=[
            #                     {"label": "csv", "value": 1},
            #                     {"label": "excel", "value": 2},
            #                     {
            #                         "label": "json",
            #                         "value": 3,
            #                     },
            #                 ],
            #             ),
            #             width=10,
            #         ),
            #     ],
            #     row=True,
            # ),
        ],
            style={
                'padding-left': '30px'
            }),
        html.Hr(),
        dcc.Upload(id='upload-data_message',
                   children=html.Div([
                       html.Button('CHOOSE FILE', id='choose_message',className='index_messagedata_add_button')
                        ]),
                   className='index_message_dataset_upload_data',
                   # Allow multiple files to be uploaded
                   multiple=True
                   ),
        html.Div([
            html.Button('ADD MESSAGE DATA', id='adding_message' ,className='index_celldata_add_button',),
            ]),
        dbc.Alert(id='alert_message', dismissable=True, is_open=False, style={'width':'500px', 'background-color':'red','font-size':'18px'})
    ], className='call_page_welcome_div'),
],
    className='call_dataset_div'
)

messagedatasetitems = [dac.SidebarMenuItem(id='add-message-records',
                                           label='Add Message Record',
                                           icon='arrow-circle-right',
                                           children=[
                                               html.Div(id="file_name_message",
                                                        style={"margin-left": "40px", 'color': 'white'})
                                           ]
                                           ),
                       ]

messagedatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=messagedatasetitems)
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

message_data_file = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    messagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Div(id='message_option', className='sample_call_data_visualize_option'),
],
    className='sample_call_dataset_div')

viewmessagedatasetitems = [dac.SidebarMenuItem(id='add-message-records',
                                               label='Add Message Record',
                                               icon='arrow-circle-right',
                                               children=html.Div(
                                                   html.Div(id="file_name_message",
                                                            style={"margin-left": "40px", 'color': 'white'})
                                               )),
                           ]

viewmessagedatasetidebar = dac.Sidebar(
    dac.SidebarMenu(
        [
            dac.SidebarHeader(children="Dataset Functions"),
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarMenuItem(id='tab_cards', label='Add a Dataset', icon='box', children=viewmessagedatasetitems)
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

############ page for view all message data
view_all_message_data = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewmessagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION - GET ALL DATA', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('VIEW DATA', outline=True, id='view_message', color='success',
                   className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', outline=True, id='close_message', color='danger',
                   className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_message_data', className='sample_call_dataset_show'),
],
    className='sample_call_dataset_div')

######## page for get all users in message dataset
get_all_message_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewmessagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION - GET ALL USERS', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize')
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('Get All Users', outline=True, color='success', id='get_message_users',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_all_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

####### page for show connected users of specific user im message dataset
connected_message_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewmessagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION - SHOW CONNECTED USERS', className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Specific User Number:", html_for="example-email"),
                dbc.Input(type="text", id="user_message", placeholder="Enter number", style={'width': '500px'}),
                dbc.FormText(
                    "Input must be a 10 digit number",
                    color="danger",
                ),
            ]
        ),
        dbc.Button('Connected Users', outline=True, color='success', id='connected_message_users',
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_connected_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

###### get message rercords between 2 users
message_records_between_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewmessagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION - MESSAGE RECORDS BETWEEN 2 USERS',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Div([
        html.H4('Enter Two Numbers:'),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("First Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="message_user2", placeholder="Enter first number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.FormGroup(
            [
                dbc.Label("Second Number", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="text", id="message_user3", placeholder="Enter second number", style={'width': '500px'}
                    ),
                    width=10,
                ),
            ],
            row=True,
        ),
        dbc.Button('Get Records', id='record_message_users', color='success', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div',
    ),
    html.Div(id='show_records_message_users', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

##### visualize connections between all users
visualize_message_connections = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    viewmessagedatasetidebar,
    html.Div([
        html.Div([
            html.H3('MESSAGE  DATASET  VISUALIZATION - VISUALIZE CONNECTIONS',
                    className='index_dataset_add_call_data')],
            className='sample_dataset_visualize'),
    ]),
    html.Hr(),
    html.Br(),
    html.Div([
        dbc.Button('Visualize Connection', id='visualize_message_connection', color='danger', outline=True,
                   className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_visualize_message_connection', className='sample_call_dataset_show_all_users'),
],
    className='sample_call_dataset_div')

message_data_list = []
update_message_data = []
message_option=[]
FilePath_message =[]

######## add message dataset 
@app.callback([Output('message-data', 'children'), Output('alert_message', 'is_open'), Output('alert_message', 'children')],
            [ Input('upload-data_message', 'filename'), Input('filepath_message', 'value'), Input('adding_message', 'n_clicks')],
              [  State('alert_message', 'is_open')]
            )
def add_message_dataset(filename, filepath, n_clicks, is_open):
    if n_clicks is not None:
        try:
            FilePath_message.append(filepath)
            filename=filename[0]
            path_File=os.path.join(filepath, filename)
            file_part=filename.split('.')
            file_type = file_part[-1]
            message_data = cz.read_msg(path_File, file_type) 
            all_users = message_data.get_all_users()
            message_data_list.append([filename, path_File, all_users, message_data])
            option=[]
            option.append(dcc.Link('◙ Show All Message Data', href='/Message_Dataset/{}/view_data'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Show All Users', href='/Message_Dataset/{}/all_users'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Show Connected Users', href='/Message_Dataset/{}/connected_users'.format(file_part[0])))
            option.append(html.Br())
            option.append(dcc.Link('◙ Message Records Between Two Selected Users', href='/Message_Dataset/{}/records_between_users'.format(file_part[0]))) 
            option.append(html.Br()) 
            option.append(dcc.Link('◙ Visualize Connections Between All Users', href='/Message_Dataset/{}/visualize_connection'.format(file_part[0]))) 
            message_option.append([file_part[0], option])
            output_message=[]
            for x in message_data_list:
                a=x[0].split('.')
                output_message.append(dcc.Link(a[0], href='/Message_Dataset/'+str(a[0])))
                output_message.append(html.Br())
            name_message=html.Div(children=output_message)
            return name_message, is_open, None

        except Exception as e:
            print(str(e))
            if str(e) == "'NoneType' object has no attribute 'get_all_users'":
                word = "File path is incorrect"
            else:
                word = "Dataset is not message dataset"
            output_message=[]
            for x in message_data_list:
                a=x[0].split('.')
                output_message.append(dcc.Link(a[0], href='/Message_Dataset/'+str(a[0])))
                output_message.append(html.Br())
            name_message=html.Div(children=output_message)
            return name_message, not is_open, word
    else:
        output_message=[]
        for x in message_data_list:
            a=x[0].split('.')
            output_message.append(dcc.Link(a[0], href='/Message_Dataset/'+str(a[0])))
            output_message.append(html.Br())
        name_message=html.Div(children=output_message)
        return name_message, False , None

@app.callback(Output('adding_message', 'n_clicks'),
              [Input('choose_message', 'n_clicks'), Input('filepath_message', 'value')])
def adding_message_button(n_clicks, filepath):
    if len(FilePath_message)>=1 and FilePath_message[-1]!=filepath:
        return None
    elif n_clicks is not None:
        return None



####### view all message data
@app.callback(Output('show_message_data', 'children'),
              [Input('view_message', 'n_clicks'), Input('close_message', 'n_clicks')
               ])
def view_message_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        message_data = update_message_data[-1][-1]
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
            # html.H2(filename_message),
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
        all_users = update_message_data[-1][2]
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


######## show connected users of specific user in message dataset
@app.callback(Output('show_connected_message_users', 'children'),
              [Input('connected_message_users', 'n_clicks'),
               Input('user_message', 'value')
               ])
def show_connected_message_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        message_data = update_message_data[-1][-1]
        all_users = update_message_data[-1][2]
        if searchUser not in all_users:
            table=html.Div([
                html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        else:
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
        message_data = update_message_data[-1][-1]
        all_users = update_message_data[-1][2]
        if user_1 not in all_users:
            table=html.Div([
                html.H5(children='User 2 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
        elif user_2 not in all_users:
            table=html.Div([
                html.H5(children='User 1 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
        else:
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
        message_data = update_message_data[-1][-1]
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

        
######## return message file name to the next page
@app.callback( dash.dependencies.Output('file_name_message', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name_message(pathname): 
    file_message = pathname.split('/')
    for a in message_option:
        if file_message[-1] == a[0]:
            for data in message_data_list:
                dataNew= data[0].split('.')
                if file_message[-1]== dataNew[0]:
                    update_message_data.append(data)
                    
            return file_message[-1]

######## get message option
@app.callback( dash.dependencies.Output('message_option', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def message_option_visu(pathname): 
    file_message = pathname.split('/')
    for a in message_option:
        if file_message[-1] == a[0]:
            return a[1]


# over message dataset
##################################################################################

@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')
               ])
def display_page(pathname):
    path_set = pathname.split('/')
    if pathname == '/Call_Dataset':
        return call_dataset
    elif pathname == '/Cell_Dataset':
        return cell_dataset
    elif pathname == '/Message_Dataset':
        return message_dataset
    elif len(path_set) == 3 and path_set[-2] == 'Call_Dataset':
        return call_dataset_file
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'view_data':
        return view_all_call_data
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'all_users':
        return get_all_users
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'connected_users':
        return connected_users
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'records_between_users':
        return records_between_users
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'close_contacts':
        return close_contacts
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'ignored_call':
        return ignore_call_detail
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'active_time':
        return active_time_user
    elif len(path_set) == 4 and path_set[-3] == 'Call_Dataset' and path_set[-1] == 'visualize_connection':
        return visualize_connections
    elif len(path_set) == 3 and path_set[-2] == 'Cell_Dataset':
        return cell_dataset_file
    elif len(path_set) == 4 and path_set[-3] == 'Cell_Dataset' and path_set[-1] == 'view_cell_data':
        return view_all_cell_data
    elif len(path_set) == 4 and path_set[-3] == 'Cell_Dataset' and path_set[-1] == 'records_cell_id':
        return records_of_cell
    elif len(path_set) == 4 and path_set[-3] == 'Cell_Dataset' and path_set[-1] == 'population_around_cell':
        return population_around_cell
    elif len(path_set) == 4 and path_set[-3] == 'Cell_Dataset' and path_set[-1] == 'trip_visualize':
        return trip_visualize
    elif len(path_set) == 3 and path_set[-2] == 'Message_Dataset':
        return message_data_file
    elif len(path_set) == 4 and path_set[-3] == 'Message_Dataset' and path_set[-1] == 'view_data':
        return view_all_message_data
    elif len(path_set) == 4 and path_set[-3] == 'Message_Dataset' and path_set[-1] == 'all_users':
        return get_all_message_users
    elif len(path_set) == 4 and path_set[-3] == 'Message_Dataset' and path_set[-1] == 'connected_users':
        return connected_message_users
    elif len(path_set) == 4 and path_set[-3] == 'Message_Dataset' and path_set[-1] == 'records_between_users':
        return message_records_between_users
    elif len(path_set) == 4 and path_set[-3] == 'Message_Dataset' and path_set[-1] == 'visualize_connection':
        return visualize_message_connections
    elif pathname == '/':
        return index_page
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
