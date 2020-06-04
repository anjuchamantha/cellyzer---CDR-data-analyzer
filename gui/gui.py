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
import pymsgbox
import flask
import os
import sys
# import ctypes

sys.path.insert(0, '../')

import cellyzer as cz

app = dash.Dash(__name__, external_stylesheets=[{dbc.themes.BOOTSTRAP}])
server = app.server

app.config.suppress_callback_exceptions = True

# image_filename = 'cdr.jpg'
# encoded_mage = base64.b64encode(open(image_filename, 'rb').read())


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

############## Other functions
def SimpleTitleBar(name="<Sub Title>"):
    return html.Div(
        dbc.NavbarSimple(
            brand=name,
            color="dark",
            dark=True,
            fluid=True,
            sticky=True,
        ),
        style={"padding-top": 20, "padding-bottom": 20, "position": "fixed", "overflow": "hidden",
                "top": 0, "width": "100rem", "background-color": "white", 'margin-left': '40px'
        }
    )

def DataSetCard(name, records="-", link=None):
    return dbc.Card(
        children=[
            dbc.CardHeader(html.H5(name, style={"text-align": "center", }), style={'background-color': 'rgba(197, 187, 187, 0.367)'}),
            dbc.CardBody(
                [
                    html.H5(records, style={"font-size": 50, "margin-bottom": 0}),
                    html.P(
                        "records", style={}
                    ),
                    html.Br(),
                    dbc.Button("Visit DataSet", color="primary", href=link, id=name),
                ],
                style={"text-align": "center"}
            ),
        ],
        style={"width": 300, "margin-right": 20, "margin-bottom": 20, 'border-style':'solid', 'border-color':'black'}
    )

def AddDataSetCard(d_type="call"):
    url = ""
    if d_type == "call":
        url = "/Call_Dataset"
        id = 'call_card'
    elif d_type == "message":
        url = "/Message_Dataset"
        id = 'message_card'
    elif d_type == "cell":
        url = "/Cell_Dataset"
        id = 'cell_card'
    return dbc.Card(
        children=[
            dbc.CardBody(
                [
                    dbc.Button("+", color="secondary", outline=True, href=url, id= id,
                               style={"font-size": 140, "height": 260, "width": 260
                                      }),
                ],
            ),
        ],
        style={"margin-bottom": 20, "width": 300}
    )

# Sidebar
homepageSidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

####### Home page
home_page = html.Div([
    SimpleTitleBar(name="Cellyzer Home Page"),
    homepageSidebar,
    html.Div(
        children=[
            dbc.Jumbotron(
                [
                    html.H1("Cellyzer", className="display-3"),
                    html.P(
                        "CELLYZER is a library to analyze "
                        "Call Detail Records.",
                        className="lead",
                    ),
                    html.Hr(className="my-2"),
                    html.P(
                        "View the documentation for more details. "
                    ),
                    html.P(dbc.Button("Visit Project Repository", color="primary"), className="lead"),
                ], style = {'padding-left': 250}
            )
        ],
        style={"margin": 20, "margin-top": 120, 'margin-left':100}

    )
], className='index_page_div')
 
###### Navbar
NavBar = html.Div(
        dbc.NavbarSimple(
            children=[
            ],
            brand="Datasets",
            color="dark",
            dark=True,
            fluid=True,
            # sticky=True,
        ),
        style={
            "padding-top": 20,
            "padding-bottom": 20,
            # "position": "fixed",
            "overflow": "hidden",
            "top": 0,
            "width": "100rem",
            "background-color": "white",
            'margin-left': '40px'
        }
    )

####### Dataset page
index_page = html.Div(children=[
    NavBar,
    homepageSidebar,
    html.Div([
        html.Div([
            html.Div([
                html.H2("Call DataSets", style={"margin-bottom": 30}),
                dbc.Row(id="call_record_home"),
            ], style={'margin-bottom': '80px'}),
            html.Div([
                html.H2("Message DataSets", style={"margin-bottom": 30}),
                dbc.Row(id="message_record_home"),
            ], style={'margin-bottom': '80px'}),
            html.Div([
                html.H2("Cell/Antena DataSets", style={"margin-bottom": 30}),
                dbc.Row(id="cell_record_home"),
            ], style={'margin-bottom': '80px'}),
        ], style={'margin-left': '50px', 'margin-top': '40px'})
    ], style={'margin': '20px', "margin-top": '40px'})
],
    className='index_page_div'
)
# over front page

################################################################################################
################################################################################################
## page for call dataset

callpagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.Div(id="call-data", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

############## page for add call data
call_dataset = html.Div([
    SimpleTitleBar(name="ADD CALL DATASET"),
    callpagesidebar,
    html.Div([
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Call DataSet File path", html_for="example-email-row", width=2, ),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath", placeholder="Ex:   D:\datasets\calls.csv",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Call Dataset Name", html_for="example-email-row", width=2, color='black'),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="upload-data_call", placeholder="How do you want to call this dataset?",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H6('Do not enter space into file name', style={'color':'red', 'font-size':15})
        ],
            style={
                'padding-left': '30px'
            }),
        html.Div([
            dbc.Button("Add DataSet", color="primary", className="mr-1 float-right", id='adding_call')
            ], style={"margin-top": '40px'}),
        dbc.Alert(id='alert', dismissable=True, is_open=False, style={'width':'500px', 'background-color':'red','font-size':'18px'})
    ], className='call_page_welcome_div', style={'margin': '20px', "margin-top": '150px'}),
],
    className='index_page_div'
)

navbar_call_dataset_file = html.Div(id= 'file_name')

callpagevisualizesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.P('Call Dataset', style={"margin-left": "40px", 'font-size':20, 'color':'white'}),
            html.Div(id="call_data_visu_sidebar", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

########### page for call dataset file visualization
call_dataset_file = html.Div([
    navbar_call_dataset_file,
    callpagevisualizesidebar,
    dbc.Row(
        children=[

            dbc.Card(
                children=[
                    dbc.CardHeader(html.H5("Available Functions", style={"text-align": "center"})),
                    dbc.CardBody(
                        html.Div(id='call_option'),
                        style={"text-align": "center"}
                    ),
                ],
                style={"margin-right": 20, "margin-bottom": 50, "width": "60%"}
            ),
        ],
        style={"margin": 20, "margin-top": 100, 'margin-left':50}

    )], className='index_page_div' )

############ page for view all call data
navbar_call_dataset_visualize = html.Div(id='navbar_call_visu')

view_all_call_data = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
    html.Div([
        dbc.Button('VIEW DATA', outline=True, id='view', color='success', className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', outline=True, id='close', color='danger', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}),
    html.Div(id='show_data', className='sample_call_dataset_show'),
],
    className='index_page_div')

######## page for get all users
get_all_users = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
    html.Div([
        dbc.Button('Get All Users', outline=True, color='success', id='get_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_all_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

####### page for show connected users of specific user
connected_users = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,    
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Specific User Number:", html_for="example-email"),
                dbc.Input(type="text", id="search", placeholder="Enter number", style={'width':'500px'}),
            ]
        ),
        dbc.Button('Connected Users', outline=True, color='success', id='connected_users', className='sample_call_dataset_viewdata'),
        ],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_connected_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

###### get call rercords between 2 users
records_between_users = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
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
            row =True,
        ),
        dbc.Button('Get Records', id='record_users', color='success', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_records_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

###### get close contacts
close_contacts = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
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
        dbc.Button('Close Contacts', id='close_contacts', color='success', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_close_contact', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

##### get ignored call details of a selected user
ignore_call_detail = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
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
        dbc.Button('Ignored Call', id='ignore_call',  color='success', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_ignore_call', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

##### get most active time of a user
active_time_user = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
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
        dbc.Button('Active Time', id='active_time', color='success', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_active_time', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

##### visualize connections between all users
visualize_connections = html.Div([
    navbar_call_dataset_visualize,
    callpagevisualizesidebar,
    html.Div([
        dbc.Button('Visualize Connection', id='visualize_connection',color='danger', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_visualize_connection', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

# over call dataset

all_file_path = []
FilePath = []
call_data_list = []
update_call_data = []
call_option=[]
call_name =[]
call_files_name = []

###### add call data
@app.callback( Output('call-data', 'children'),
            [  Input('upload-data_call', 'value'), Input('filepath', 'value'), Input('adding_call', 'n_clicks')],
            )
def add_call_dataset(filename, filepath, n_clicks):
    if n_clicks is not None:
        try:
            FilePath.append(filepath)
            call_files_name.append(filename)
            path_File=filepath
            if path_File in all_file_path or filename in call_name or ' ' in filename:
                output_call=[]
                for x in call_data_list:
                    a=x[0]
                    output_call.append(dcc.Link(a, href='/Call_Dataset/'+str(a)))
                    output_call.append(html.Br())
                name=html.Div(children=output_call)
                return name
            else:
                file_part=filepath.split('\\')
                file_call = file_part[-1].split('.')
                file_type = file_call[-1]
                call_data = cz.read_call(path_File, file_type)
                record = call_data.get_records() 
                all_users = call_data.get_all_users()
                call_data_list.append([filename, path_File, all_users, record, call_data])
                all_file_path.append(path_File)
                call_name.append(filename)
                option=[]
                option.append(dbc.Row(dbc.Button("Show All Data", href='/Call_Dataset/{}/view_data'.format(filename), color="light", className="mr-1", block=True, id='visu_show_call',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Show All the users", href='/Call_Dataset/{}/all_users'.format(filename), color="light", className="mr-1", block=True, id='visu_call_users',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Show connected users", href='/Call_Dataset/{}/connected_users'.format(filename), color="light", className="mr-1", block=True, id='visu_call_connected',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Call records between 2 selected users", href='/Call_Dataset/{}/records_between_users'.format(filename), color="light", className="mr-1", block=True, id='visu_call_records',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Close contacts of selected users", href='/Call_Dataset/{}/close_contacts'.format(filename), color="light", className="mr-1", block=True, id='visu_call_close',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Ignored Call details of a given user", href='/Call_Dataset/{}/ignored_call'.format(filename), color="light", className="mr-1", block=True, id='visu_ignored_call',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Active time of a given user", href='/Call_Dataset/{}/active_time'.format(filename), color="light", className="mr-1", block=True, id='visu_active_time',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button(["Visualize connections between all users ",
                                dbc.Badge("Heavy Function", color="danger", className="mr-1")],
                               color="light",
                               className="mr-1",
                               id='visu_call_visu_connection',
                               block=True,
                               style={"margin-bottom": 10, "text-align": 'start'}, href='/Call_Dataset/{}/visualize_connection'.format(filename))))
                call_option.append([filename, option])
                output_call=[]
                for x in call_data_list:
                    a=x[0]
                    output_call.append(dcc.Link(a, href='/Call_Dataset/'+str(a)))
                    output_call.append(html.Br())
                name=html.Div(children=output_call)
                return name

        except Exception as e:
            print(str(e))
            output_call=[]
            for x in call_data_list:
                a=x[0]               
                output_call.append(dcc.Link(a, href='/Call_Dataset/'+str(a)))
                output_call.append(html.Br())
            name=html.Div(children=output_call)
            return name
        
    else:
        output_call=[]
        for x in call_data_list:
            a=x[0]        
            output_call.append(dcc.Link(a, href='/Call_Dataset/'+str(a)))
            output_call.append(html.Br())
        name=html.Div(children=output_call)
        return name


########### alert for call data
@app.callback( [ Output('alert', 'is_open'), Output('alert', 'children')],
            [  Input('upload-data_call', 'value'), Input('filepath', 'value'), Input('adding_call', 'n_clicks')],
             [  State('alert', 'is_open')]
            )
def add_call_dataset_alert(filename, filepath, n_clicks, is_open):
    if n_clicks is not None:
        try:
            if filepath is None:
                word = 'Please enter filepath'
                return True, word
            elif filename is None:
                word = 'Please enter filename'
                return True, word
            elif filepath in all_file_path:
                word = 'This file already exist'
                return True, word
            elif filename in call_name:
                word = 'Please enter other name'
                return True, word
            elif ' ' in filename:
                word = 'Do not enter space into filename'
                return True, word
            else:
                path_File=filepath 
                file_part=filepath.split('\\')
                file_call = file_part[-1].split('.')
                file_type = file_call[-1]
                call_data = cz.read_call(path_File, file_type)
                all_users = call_data.get_all_users()

                return False, None

        except Exception as e:
            print(e)
            if str(e) == "'NoneType' object has no attribute 'get_all_users'":
                word = "File path is incorrect"
            else:
                word = "Dataset is not call dataset"
            return True, word
        
    else:
        return False, None

######## direct for the datset page after adding call dataset
@app.callback(  Output('adding_call', 'href'),
            [  Input('upload-data_call', 'value'), Input('filepath', 'value')]
            )
def call_direct_datset(filename, filepath):
    try:
        path_File=filepath 
        file_part=filepath.split('\\')
        file_call = file_part[-1].split('.')
        file_type = file_call[-1]
        call_data = cz.read_call(path_File, file_type)
        all_users = call_data.get_all_users()
        if (filename in call_name) or (path_File in all_file_path) or (filepath is None) or (filename is None) or (' ' in filename):
            return None
        else:
            href = '/Dataset'
            return href

    except Exception as e:
        # print(e)
        return None

########## set n_clicks to 0        
@app.callback(Output('adding_call', 'n_clicks'),
              [Input('upload-data_call', 'value'), Input('filepath', 'value')])
def adding_call_button(filename, filepath):
    if len(FilePath)>=1 and FilePath[-1]!=filepath:
        return None
    elif len(call_files_name)>=1 and call_files_name[-1]!=filename:
        return None


######## return call file name to the next page
@app.callback( dash.dependencies.Output('file_name', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name_call(pathname): 
    file_call = pathname.split('/')
    for a in call_option:
        if len(file_call)>2 and file_call[2] == a[0]:
            for data in call_data_list:
                dataNew= data[0].split('.')
                if file_call[2]== dataNew[0]:
                    update_call_data.append(data)

            name = "Call Dataset :<%s>" % file_call[2]
            return SimpleTitleBar(name)

######## return call records card to the home page
@app.callback( dash.dependencies.Output('call_record_home', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def call_record_card_home(pathname):
    if len(call_data_list)>0 :
        call_data_name = []
        for x in call_data_list:
            a=x[0]
            record = len(x[3])
            link = '/Call_Dataset/'+str(a)
            call_data_name.append(DataSetCard(a, record, link))
        call_data_name.append(AddDataSetCard('call'))
        return call_data_name

    else:
        return AddDataSetCard('call')

########### get call visualize option for navigation bar
@app.callback( dash.dependencies.Output('navbar_call_visu', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def get_navbar_visu_call(pathname):
    path_set = pathname.split('/')
    if len(path_set)==4 and path_set[-3]== 'Call_Dataset':
        if path_set[-1]=='view_data':
            return SimpleTitleBar("Call Dataset :<%s> => All Data" % path_set[-2])
        elif path_set[-1]=='all_users':
            return SimpleTitleBar("Call Dataset :<%s> => All Users" % path_set[-2])
        elif path_set[-1]=='connected_users':
            return SimpleTitleBar("Call Dataset :<%s> => Connected Users" % path_set[-2])
        elif path_set[-1]== 'records_between_users':
            return SimpleTitleBar("Call Dataset :<%s> => Records Between Users" % path_set[-2])
        elif path_set[-1]== 'close_contacts':
            return SimpleTitleBar("Call Dataset :<%s> => Close Contacts" % path_set[-2])
        elif path_set[-1]== 'ignored_call':
            return SimpleTitleBar("Call Dataset :<%s> => Ignore Call" % path_set[-2])
        elif path_set[-1]== 'active_time':
            return SimpleTitleBar("Call Dataset :<%s> => Active Time" % path_set[-2])
        elif path_set[-1]== 'visualize_connection':
            return SimpleTitleBar("Call Dataset :<%s> => Visualize Connection" % path_set[-2])

######## get call option
@app.callback( dash.dependencies.Output('call_option', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name2(pathname): 
    file_call = pathname.split('/')
    for a in call_option:
        if len(file_call)>2 and file_call[2] == a[0]:
            return a[1]

######## return all call file names into call visualize sidebar
@app.callback( dash.dependencies.Output('call_data_visu_sidebar', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def call_visu_sidebar(pathname):
    if len(call_data_list)>=1:
        output_call=[]
        for x in call_data_list:
            a=x[0]        
            output_call.append(dcc.Link(a, href='/Call_Dataset/'+str(a)))
            output_call.append(html.Br())
        name=html.Div(children=output_call)
        return name

######### view call dataset
@app.callback(Output('show_data', 'children'),
              [ Input('view', 'n_clicks'),
                Input('close', 'n_clicks')
               ])
def update_table(n_clicks, click2):
    try:
        table = html.Div()
        if click2 is not None:
            return None

        if n_clicks is not None:
            record_call = update_call_data[-1][3]
            dict_list = []
            for record in record_call:
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
                html.Table(children=tab,
                        style={'border-collapse': 'collapse',
                                'border': '1px solid black',
                                'width': '100%'
                                })
            ])
            return table

    except Exception as e:
        print(e)

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
        try:
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

        except Exception as e:
            print(e)


connected_userList = []
######## show connected users of specific user
@app.callback(Output('show_connected_users', 'children'),
              [Input('connected_users', 'n_clicks'),
               Input('search', 'value')
               ])
def show_connected_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        connected_userList.append(searchUser)
        try:
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            if searchUser is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif searchUser not in call_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            else:
                connected_users = call_data.get_connected_users(searchUser)
                if len(connected_users)==0:
                    table=html.Div([
                        html.H5(children='No connected users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
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

        except Exception as e:
            print(e)

###### set 0 n_clicks connected user button
@app.callback(Output('connected_users', 'n_clicks'),
              [Input('search', 'value')])
def conneced_users_button(user):
    if len(connected_userList)>=1 and connected_userList[-1]!=user:
        return None


record_user1 = []
record_user2 = []
####### show records between 2 input users
@app.callback(Output('show_records_users', 'children'),
              [Input('search_3', 'value'),
               Input('search_2', 'value'),
               Input('record_users', 'n_clicks')
               ])
def between_users_records(user_1, user_2, click):
    table = html.Div()

    if click is not None:
        record_user1.append(user_1)
        record_user2.append(user_2)
        try:
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            dict_list = []
            if user_1 is None or user_2 is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_2 not in call_users:
                table=html.Div([
                    html.H5(children='User 1 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_1 not in call_users:
                table=html.Div([
                    html.H5(children='User 2 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
                for record in call_data.get_records(user_1, user_2):
                    dict_list.append(vars(record))
                # header = list(dict_list[0].keys())              
                if len(dict_list)==0:
                    table=html.Div([
                        html.H5(children='No records between two users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
                else:
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

        except Exception as e:
            print(e)

###### set 0 n_clicks record_users button
@app.callback(Output('record_users', 'n_clicks'),
              [Input('search_3', 'value'), Input('search_2', 'value')])
def record_users_button(user1, user2):
    if len(record_user1)>=1 and record_user1[-1] != user1:
        return None
    elif len(record_user2)>=1 and record_user2[-1] != user2:
        return None


close_contactList = []
numberList = []
######## show close contacts
@app.callback(Output('show_close_contact', 'children'),
              [Input('user_3', 'value'),
               Input('contact', 'value'),
               Input('close_contacts', 'n_clicks')
               ])
def show_close_contatcs(user_3, contact, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        try:
            close_contactList.append(user_3)
            numberList.append(contact)
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            if user_3 is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_3 not in call_users:
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
        
        except Exception as e:
            print(e)      

###### set 0 n_clicks close_contacts button
@app.callback(Output('close_contacts', 'n_clicks'),
              [Input('user_3', 'value'), Input('contact', 'value')])
def close_contacts_button(user, contact):
    if len(close_contactList)>=1 and close_contactList[-1] != user:
        return None
    elif len(numberList)>=1 and numberList[-1] != contact:
        return None


active_timeList = []
######## show most active time
@app.callback(Output('show_active_time', 'children'),
              [Input('active_time', 'n_clicks'),
               Input('user_4', 'value')
               ])
def show_active_time(n_clicks, user_4):
    table = html.Div()
    try:
        if n_clicks is not None:
            active_timeList.append(user_4)
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            if user_4 is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_4 not in call_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])          
            else:
                active_time = call_data.get_most_active_time(user_4)
                cz.visualization.active_time_bar_chart(active_time)
            return table
    
    except Exception as e:
        print(e)

###### set 0 n_clicks active_time button
@app.callback(Output('active_time', 'n_clicks'),
              [Input('user_4', 'value')])
def active_time_button(user):
    if len(active_timeList)>=1 and active_timeList[-1] != user:
        return None 


ignored_callList = []
######### Show ignored call
@app.callback(Output('show_ignore_call', 'children'),
              [Input('user_5', 'value'),
               Input('ignore_call', 'n_clicks')
               ])
def show_ignore_call(user_5, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        ignored_callList.append(user_5)
        try:
            call_data = update_call_data[-1][-1]
            call_users = update_call_data[-1][2]
            if user_5 is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_5 not in call_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
                ignore_call = call_data.get_ignored_call_details(user_5)
                if len(ignore_call) == 0:
                    table=html.Div([
                        html.H5(children='No records between two users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
                else:
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

        except Exception as e:
            print(e)

###### set 0 n_clicks ignore_call button
@app.callback(Output('ignore_call', 'n_clicks'),
              [Input('user_5', 'value')])
def ignore_call_button(user):
    if len(ignored_callList)>=1 and ignored_callList[-1] != user:
        return None 


###### Visualize connection betwwen all users
@app.callback(Output('show_visualize_connection', 'children'),
              [Input('visualize_connection', 'n_clicks')
               ])
def show_visualize_connection(n_clicks):
    try:
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

    except Exception as e:
        print(e)


###################################################################################################
###################################################################################################

## Page for cell dataset

cellpagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.Div(id="cell-data", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

############ add cell dataset
cell_dataset = html.Div([
    SimpleTitleBar(name="ADD CELL/ANTENNA DATASET"),
    cellpagesidebar,
    html.Div([
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Cell DataSet File path", html_for="example-email-row", width=2, ),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath_cell", placeholder="Ex:   D:\datasets\cells.csv",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Cell Dataset Name", html_for="example-email-row", width=2, color='black'),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="upload-data_cell", placeholder="How do you want to call this dataset?",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H6('Do not enter space into file name', style={'color':'red', 'font-size':15}),
            html.Br(),
            dbc.FormGroup(
                [
                    dbc.Label("Select Call Dataset", html_for="dropdown", width=2),
                    dbc.Col(
                        dcc.Dropdown(
                            id="select_call",
                            placeholder="Select the Call Dataset to link",
                            style = {'width':800}
                        ),
                    ),
                ],
                row=True,
                style={"margin-bottom": 20}
            ),
            html.H6('Add call dataset before adding cell dataset', style={'color':'red', 'font-size':15}),
        ],
            style={
                'padding-left': '30px'
            }),
        html.Div([
            dbc.Button("Add DataSet", color="primary", className="mr-1 float-right", id='show_cell_dash')
            ], style={"margin-top": '40px'}),
        dbc.Alert(id='alert_cell', dismissable=True, is_open=False, style={'width':'500px', 'background-color':'red','font-size':'18px'})
    ], className='call_page_welcome_div', style={'margin': '20px', "margin-top": '150px'}),
],
    className='index_page_div'
)


############## navbar for cell_dataset_file page
navbar_cell_dataset_file = html.Div(id= 'file_name_cell')

############# side navbar for cell dataset visualization
cellpagevisualizesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.P('Cell Dataset', style={"margin-left": "40px", 'font-size':20, 'color':'white'}),
            html.Div(id="cell_data_visu_sidebar", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

########### page for call dataset file visualization
cell_dataset_file = html.Div([
    navbar_cell_dataset_file,
    cellpagevisualizesidebar,
    dbc.Row(
        children=[

            dbc.Card(
                children=[
                    dbc.CardHeader(html.H5("Available Functions", style={"text-align": "center"})),
                    dbc.CardBody(
                        html.Div(id='cell_option'),
                        style={"text-align": "center"}
                    ),
                ],
                style={"margin-right": 20, "margin-bottom": 50, "width": "60%"}
            ),
        ],
        style={"margin": 20, "margin-top": 100, 'margin-left':50}

    )], className='index_page_div' )


############ navbar for cell dataset visualization
navbar_cell_dataset_visualize = html.Div(id='navbar_cell_visu')

############ page for view all cell data
view_all_cell_data = html.Div([
    navbar_cell_dataset_visualize,
    cellpagevisualizesidebar,
    html.Div([
        dbc.Button('VIEW DATA', id='view_cell', outline=True, color='success', className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', id='close_cell', outline=True, color='danger', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}),
    html.Div(id='show_cell_data', className='sample_call_dataset_show'),
],
    className='index_page_div')

###### get records of specific cell
records_of_cell = html.Div([
    navbar_cell_dataset_visualize,
    cellpagevisualizesidebar,
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
        dbc.Button('Records Cell', id='records_cell', outline=True, color='success', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_records_cell', className='ndex_dataset_cell_record_div'),
],
    className='index_page_div')

######## page for get population and visualize
population_around_cell = html.Div([
    navbar_cell_dataset_visualize,
    cellpagevisualizesidebar,
    html.Div([
        dbc.Button('Get Population', id='population_button', outline=True, color='danger', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_population', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

######## page for trip visualization
trip_visualize = html.Div([
    navbar_cell_dataset_visualize,
    cellpagevisualizesidebar,

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
        dbc.Button('Trip Visualize', id='trip_visualize_button', outline=True, color='danger', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_trip_visualize', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

########### over cell pages

cell_data_list = []
update_cell_data = []
cell_option = []
File_Path_cell =[]
all_file_path_cell = []
adding_call = []
cell_file_name =[]
added_cell_name = []


####### add cell data
@app.callback(  Output('cell-data', 'children'),
              [  Input('select_call', 'value'), Input('upload-data_cell', 'value'), Input('filepath_cell', 'value'), Input('show_cell_dash', 'n_clicks')],
            )
def add_cell_dataset(call_file, filename, filepath, n_clicks):
    if n_clicks is not None:
        try:
            File_Path_cell.append(filepath)
            adding_call.append(call_file)
            cell_file_name.append(filename)
            path_File = filepath
            if path_File in all_file_path_cell or filename in added_cell_name or ' ' in filename:
                output_cell=[]
                for x in cell_data_list:
                    a=x[0]
                    output_cell.append(dcc.Link(a, href='/Cell_Dataset/'+str(a)))
                    output_cell.append(html.Br())
                name_cell=html.Div(children = output_cell)
                return name_cell
            else:
                file_part=filepath.split('\\')
                file_cell = file_part[-1].split('.')
                file_type = file_cell[-1]
                for call in call_data_list:
                    f_name= call[0]
                    if call_file == f_name:
                        cell_data = cz.read_cell(path_File, call[1], call[-1], file_type)
                        dict_list = []
                        cell_record = cell_data.get_records()
                        for record in cell_record:
                            dict_list.append(vars(record))
                        cell_data_list.append([filename, path_File, call[2], cell_record, cell_data])
                        all_file_path_cell.append(path_File)
                        added_cell_name.append(filename)
                        break
                option=[]
                option.append(dbc.Row(dbc.Button("Show All Data", href='/Cell_Dataset/{}/view_cell_data'.format(filename), color="light", className="mr-1", block=True, id='visu_cell_data',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Records Of a Specific Cell", href='/Cell_Dataset/{}/records_cell_id'.format(filename), color="light", className="mr-1", block=True, id='visu_cell_id',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Population Around Cell", href='/Cell_Dataset/{}/population_around_cell'.format(filename), color="light", className="mr-1", block=True, id='visu_population',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Trip Visualization", href='/Cell_Dataset/{}/trip_visualize'.format(filename), color="light", className="mr-1", block=True, id='visu_trip_visualization', 
                               style={"margin-bottom": 10, "text-align": 'start'})))
                cell_option.append([filename, option])
                output_cell=[]
                for x in cell_data_list:
                    a=x[0]
                    output_cell.append(dcc.Link(a, href='/Cell_Dataset/'+str(a)))
                    output_cell.append(html.Br())
                name_cell=html.Div(children = output_cell)
                return name_cell

        except Exception as e:
            print(str(e))
            output_cell=[]
            for x in cell_data_list:
                a=x[0]
                output_cell.append(dcc.Link(a, href='/Cell_Dataset/'+str(a)))
                output_cell.append(html.Br())
            name_cell=html.Div(children = output_cell)
            return name_cell

    else :
        output_cell=[]
        for x in cell_data_list:
            a=x[0]
            output_cell.append(dcc.Link(a, href='/Cell_Dataset/'+str(a)))
            output_cell.append(html.Br())
        name_cell=html.Div(children = output_cell)
        return name_cell


############## error alert for cell data
@app.callback([  Output('alert_cell', 'is_open'), Output('alert_cell', 'children')],
              [  Input('select_call', 'value'), Input('upload-data_cell', 'value'), Input('filepath_cell', 'value'), Input('show_cell_dash', 'n_clicks')],
              [  State('alert_cell', 'is_open')] 
            )
def add_cell_dataset_alert(call_file, filename, filepath, n_clicks, is_open):
    if n_clicks is not None:
        try:
            if filepath is None:
                word = 'Please enter filepath'
                return True, word
            elif filename is None:
                word = 'Please enter filename'
                return True, word
            elif call_file is None:
                word = 'Please add call dataset'
                return True, word
            elif filepath in all_file_path_cell:
                word = 'This file already exist'
                return True, word
            elif filename in added_cell_name:
                word = 'Please enter other name'
                return True, word
            elif ' ' in filename:
                word = 'Do not enter space into filename'
                return True, word
            else:
                path_File = filepath
                file_part=filepath.split('\\')
                file_cell = file_part[-1].split('.')
                file_type = file_cell[-1]
                for call in call_data_list:
                    f_name= call[0]
                    if call_file == f_name:
                        cell_data = cz.read_cell(path_File, call[1], call[-1], file_type)
                        dict_list = []
                        for record in cell_data.get_records():
                            dict_list.append(vars(record))
                        break
                return False, None

        except Exception as e:
            print(str(e))
            if str(e) == "'NoneType' object has no attribute 'get_records'":
                word = "File path is incorrect"
            elif str(e) == "local variable 'cell_data' referenced before assignment":
                word = "Incorrect call dataset"
            else:
                word = "Dataset is not cell dataset"
            return  True, word

    else :
        return False , None

######## direct for the datset page after adding cell dataset
@app.callback(  Output('show_cell_dash', 'href'),
            [  Input('select_call', 'value'), Input('upload-data_cell', 'value'), Input('filepath_cell', 'value')]
            )
def cell_direct_datset(call_file, filename, filepath):
    try:
        path_File = filepath
        file_part=filepath.split('\\')
        file_cell = file_part[-1].split('.')
        file_type = file_cell[-1]
        for call in call_data_list:
            f_name= call[0]
            if call_file == f_name:
                cell_data = cz.read_cell(path_File, call[1], call[-1], file_type)
                dict_list = []
                for record in cell_data.get_records():
                    dict_list.append(vars(record))
                break
        if (filename in added_cell_name) or (path_File in all_file_path_cell) or (filepath is None) or (filename is None) or (call_file is None) or (' ' in filename):
            return None
        else:
            href = '/Dataset'
            return href

    except Exception as e:
        # print(e)
        return None


########### set button n_clicks to zero
@app.callback(Output('show_cell_dash', 'n_clicks'),
              [ Input('select_call', 'value'), Input('upload-data_cell', 'value'), Input('filepath_cell', 'value')])
def adding_cell_button(call_file, filename, filepath):
    if len(File_Path_cell)>=1 and File_Path_cell[-1]!=filepath:
        return None
    elif len(cell_file_name)>=1 and cell_file_name[-1]!=filename:
        return None
    elif len(adding_call)>=1 and adding_call[-1]!=call_file:
        return None


########### show cell data
@app.callback(Output('show_cell_data', 'children'),
              [ Input('view_cell', 'n_clicks'), 
                Input('close_cell', 'n_clicks')
               ])
def view_cell_data(n_clicks, click2):
    try:
        table = html.Div()
        if click2 is not None:
            return None

        if n_clicks is not None:
            cell_records = update_cell_data[-1][3]
            dict_list = []
            for record in cell_records:
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
                html.Table(children=tab,
                        style={'border-collapse': 'collapse',
                                'border': '1px solid black',
                                'width': '100%'
                                })
            ])
            return table

    except Exception as e:
        print(e)

#### set 0 to n_clicks in close_cell
@app.callback(Output('close_cell', 'n_clicks'),
              [Input('view_cell', 'n_clicks')
               ])
def close_cell_data(n_clicks):
    if n_clicks is not None:
        return None

######## select call dataset using dropdown
@app.callback(Output('select_call', 'options'),
            [   Input('filepath_cell', 'value')
            ])
def get_call_for_cell(filepath):
    if filepath is not None and len(call_data_list)>=1:
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
    try:
        if n_clicks is not None:
            antana_dataset = update_cell_data[-1][-1]
            population = antana_dataset.get_population()
            return cz.visualization.cell_population_visualization(population)

    except Exception as e:
        print(e)


trip_userList = []
######### get trip visualize
@app.callback(Output('show_trip_visualize', 'children'),
              [Input('trip_user', 'value'),
               Input('trip_visualize_button', 'n_clicks')
               ])
def trip_visualization(user, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        trip_userList.append(user)
        try:
            all_users= update_cell_data[-1][2]
            if user is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            elif user not in all_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
                antana_dataset = update_cell_data[-1][-1]
                trip_visualize = antana_dataset.get_trip_details(user)
                cz.visualization.trip_visualization(trip_visualize)
            return table

        except Exception as e:
            print(e)

###### set 0 n_clicks trip_visualize_button button
@app.callback(Output('trip_visualize_button', 'n_clicks'),
              [Input('trip_user', 'value')])
def trip_visualize_button_button(user):
    if len(trip_userList)>=1 and trip_userList[-1] != user:
        return None 


######## return cell file name to the next page
@app.callback( dash.dependencies.Output('file_name_cell', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name_cell(pathname): 
    file_cell = pathname.split('/')
    for a in cell_option:
        if len(file_cell)>2 and file_cell[2] == a[0]:
            for data in cell_data_list:
                dataNew= data[0].split('.')
                if file_cell[2]== dataNew[0]:
                    update_cell_data.append(data)

            name = "Cell Dataset :<%s>" % file_cell[2]
            return SimpleTitleBar(name)              

######## get cell option
@app.callback( dash.dependencies.Output('cell_option', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def cell_option_visu(pathname): 
    file_cell = pathname.split('/')
    for a in cell_option:
        if len(file_cell)>2 and file_cell[2] == a[0]:
            return a[1]

######## return cell records card to the home page
@app.callback( dash.dependencies.Output('cell_record_home', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def cell_record_card_home(pathname):
    if len(cell_data_list)>0 :
        cell_data_name = []
        for x in cell_data_list:
            a=x[0]
            record = len(x[3])
            link = '/Cell_Dataset/'+str(a)
            cell_data_name.append(DataSetCard(a, record, link))
        cell_data_name.append(AddDataSetCard('cell'))
        return cell_data_name
    else:
        return AddDataSetCard('cell')


########### get cell visualize option for navigation bar
@app.callback( dash.dependencies.Output('navbar_cell_visu', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def get_navbar_visu_cell(pathname):
    path_set = pathname.split('/')
    if len(path_set)==4 and path_set[-3]== 'Cell_Dataset':
        if path_set[-1]=='view_cell_data':
            return SimpleTitleBar("Cell Dataset :<%s> => All Data" % path_set[-2])
        elif path_set[-1]=='records_cell_id':
            return SimpleTitleBar("Cell Dataset :<%s> => Records Of a Specific Cell" % path_set[-2])
        elif path_set[-1]=='population_around_cell':
            return SimpleTitleBar("Cell Dataset :<%s> => Population Around Cell" % path_set[-2])
        elif path_set[-1]=='trip_visualize':
            return SimpleTitleBar("Cell Dataset :<%s> => Trip Visualization" % path_set[-2])


######## return all cell file names into cell visualize sidebar
@app.callback( dash.dependencies.Output('cell_data_visu_sidebar', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def cell_visu_sidebar(pathname):
    if len(call_data_list)>=1:
        output_cell=[]
        for x in cell_data_list:
            a=x[0]
            output_cell.append(dcc.Link(a, href='/Cell_Dataset/'+str(a)))
            output_cell.append(html.Br())
        name_cell=html.Div(children = output_cell)
        return name_cell

# over cell callback

################################################################################################
################################################################################################

## Page for message dataset

messagepagesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.Div(id="message-data", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

###### add message dataset
message_dataset = html.Div([
    SimpleTitleBar(name="ADD MESSAGE DATASET"),
    messagepagesidebar,
    html.Div([
        html.Div([
            dbc.FormGroup(
                [
                    dbc.Label("Message DataSet File path", html_for="example-email-row", width=2, ),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="filepath_message", placeholder="Ex:   D:\datasets\messages.csv",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            dbc.FormGroup(
                [
                    dbc.Label("Message Dataset Name", html_for="example-email-row", width=2, color='black'),
                    dbc.Col(
                        dbc.Input(
                            type="text", id="upload-data_message", placeholder="How do you want to call this dataset?",
                            style={'width': '800px'}
                        ),
                        width=10,
                    ),
                ],
                row=True,
            ),
            html.H6('Do not enter space into file name', style={'color':'red', 'font-size':15})
        ],
            style={
                'padding-left': '30px'
            }),
        html.Div([
            dbc.Button("Add DataSet", color="primary", className="mr-1 float-right", id='adding_message')
            ], style={"margin-top": '40px'}),
        dbc.Alert(id='alert_message', dismissable=True, is_open=False, style={'width':'500px', 'background-color':'red','font-size':'18px'})
    ], className='call_page_welcome_div', style={'margin': '20px', "margin-top": '150px'}),
],
    className='index_page_div'
)

########### navbar for message dataset file
navbar_message_dataset_file = html.Div(id= 'file_name_message')

#########  sidebar for message visualization
messagepagevisualizesidebar = dac.Sidebar(
    dac.SidebarMenu(
        [   
            dac.SidebarButton(id='add-cell-records', label='Home', icon='home', href='/'),
            dac.SidebarButton(id='add-cell-records-dataset', label='Dataset', icon='box', href='/Dataset'),
            html.P('Message Dataset', style={"margin-left": "40px", 'font-size':20, 'color':'white'}),
            html.Div(id="message_data_visu_sidebar", style={"margin-left": "40px"})
        ]
    ),
    title='CELLYZER',
    color="primary",
    brand_color="secondary",
    src="https://adminlte.io/themes/AdminLTE/dist/img/user2-160x160.jpg",
    elevation=3,
    opacity=0.8
)

########### page for message dataset file visualization
message_data_file = html.Div([
    navbar_message_dataset_file,
    messagepagevisualizesidebar,
    dbc.Row(
        children=[

            dbc.Card(
                children=[
                    dbc.CardHeader(html.H5("Available Functions", style={"text-align": "center"})),
                    dbc.CardBody(
                        html.Div(id='message_option'),
                        style={"text-align": "center"}
                    ),
                ],
                style={"margin-right": 20, "margin-bottom": 50, "width": "60%"}
            ),
        ],
        style={"margin": 20, "margin-top": 100, 'margin-left':50}

    )], className='index_page_div' )

################### navbar for message visualization
navbar_message_dataset_visualize = html.Div(id='navbar_message_visu')

############ page for view all message data
view_all_message_data = html.Div([
    navbar_message_dataset_visualize,
    messagepagevisualizesidebar,
    html.Div([
        dbc.Button('VIEW DATA', outline=True, id='view_message', color='success', className='sample_call_dataset_viewdata'),
        dbc.Button('CLOSED DATA', outline=True, id='close_message', color='danger', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}),
    html.Div(id='show_message_data', className='sample_call_dataset_show'),
    ],
    className='index_page_div')

######## page for get all users in message dataset
get_all_message_users = html.Div([
    navbar_message_dataset_visualize,
    messagepagevisualizesidebar,
    html.Div([
        dbc.Button('Get All Users', outline=True, color='success', id='get_message_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_all_message_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

####### page for show connected users of specific user im message dataset
connected_message_users = html.Div([
    navbar_message_dataset_visualize,
    messagepagevisualizesidebar,
    html.Div([
        dbc.FormGroup(
            [
                dbc.Label("Enter Specific User Number:", html_for="example-email"),
                dbc.Input(type="text", id="user_message", placeholder="Enter number", style={'width':'500px'}),
            ]
        ),
        dbc.Button('Connected Users', outline=True, color='success', id='connected_message_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_connected_message_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

###### get message rercords between 2 users
message_records_between_users = html.Div([
    navbar_message_dataset_visualize,
    messagepagevisualizesidebar,
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
        dbc.Button('Get Records', id='record_message_users', color='success', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_records_message_users', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

##### visualize connections between all users
visualize_message_connections = html.Div([
    navbar_message_dataset_visualize,
    messagepagevisualizesidebar,
    html.Div([
        dbc.Button('Visualize Connection', id='visualize_message_connection',color='danger', outline=True, className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div', style={"margin": 20, "margin-top": 100}
    ),
    html.Div(id='show_visualize_message_connection', className='sample_call_dataset_show_all_users'),
],
    className='index_page_div')

##############

message_data_list = []
update_message_data = []
message_option=[]
FilePath_message =[]
all_message_path = []
file_name_message = []
added_message_name =[]

######## add message dataset 
@app.callback(Output('message-data', 'children'),
            [ Input('upload-data_message', 'value'), Input('filepath_message', 'value'), Input('adding_message', 'n_clicks')],
            )
def add_message_dataset(filename, filepath, n_clicks):
    if n_clicks is not None:
        try:
            FilePath_message.append(filepath)
            file_name_message.append(filename)
            path_File=filepath
            if path_File in all_message_path or filename in added_message_name or ' ' in filename:
                output_message=[]
                for x in message_data_list:
                    a=x[0]
                    output_message.append(dcc.Link(a, href='/Message_Dataset/'+str(a)))
                    output_message.append(html.Br())
                name_message=html.Div(children=output_message)
                return name_message 
            else:               
                file_part=filepath.split('\\')
                file_message = file_part[-1].split('.')
                file_type = file_message[-1]
                message_data = cz.read_msg(path_File, file_type) 
                all_users = message_data.get_all_users()
                message_record = message_data.get_records()
                message_data_list.append([filename, path_File, all_users, message_record, message_data])
                all_message_path.append(path_File)
                added_message_name.append(filename)
                option=[]
                option.append(dbc.Row(dbc.Button("Show All Data", href='/Message_Dataset/{}/view_data'.format(filename), color="light", className="mr-1", block=True, id='visu_message_data',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Show All the users", href='/Message_Dataset/{}/all_users'.format(filename), color="light", className="mr-1", block=True, id='visu_message_users',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Show connected users", href='/Message_Dataset/{}/connected_users'.format(filename), color="light", className="mr-1", block=True, id='visu_message_connected',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button("Message records between 2 selected users", href='/Message_Dataset/{}/records_between_users'.format(filename), color="light", className="mr-1", block=True, id='visu_message_records_2',
                               style={"margin-bottom": 10, "text-align": 'start'})))
                option.append(dbc.Row(dbc.Button(["Visualize connections between all users ",
                                dbc.Badge("Heavy Function", color="danger", className="mr-1")],
                               color="light",
                               id='visu_message_visualization',
                               className="mr-1",
                               block=True,
                               style={"margin-bottom": 10, "text-align": 'start'}, href='/Message_Dataset/{}/visualize_connection'.format(filename)))) 
                message_option.append([filename, option])
                output_message=[]
                for x in message_data_list:
                    a=x[0]
                    output_message.append(dcc.Link(a, href='/Message_Dataset/'+str(a)))
                    output_message.append(html.Br())
                name_message=html.Div(children=output_message)
                return name_message 

        except Exception as e:
            print(str(e))
            output_message=[]
            for x in message_data_list:
                a=x[0]
                output_message.append(dcc.Link(a, href='/Message_Dataset/'+str(a)))
                output_message.append(html.Br())
            name_message=html.Div(children=output_message)
            return name_message 
    else:
        output_message=[]
        for x in message_data_list:
            a=x[0]
            output_message.append(dcc.Link(a, href='/Message_Dataset/'+str(a)))
            output_message.append(html.Br())
        name_message=html.Div(children=output_message)
        return name_message 


######### show message alert 
@app.callback([Output('alert_message', 'is_open'), Output('alert_message', 'children')],
            [ Input('upload-data_message', 'value'), Input('filepath_message', 'value'), Input('adding_message', 'n_clicks')],
              [  State('alert_message', 'is_open')]
            )
def add_message_dataset_alert(filename, filepath, n_clicks, is_open):
    if n_clicks is not None:
        try:
            if filepath is None:
                word = 'Please enter filepath'
                return True, word
            elif filename is None:
                word = 'Please enter filename'
                return True, word
            elif filepath in all_message_path:
                word = 'This file already exist'
                return True, word
            elif filename in added_message_name:
                word = 'Please enter other name'
                return True, word
            elif ' ' in filename:
                word = 'Do not enter space into filename'
                return True, word
            else:
                path_File=filepath 
                file_part=filepath.split('\\')
                file_message = file_part[-1].split('.')
                file_type = file_message[-1]
                cz.read_msg(path_File, file_type) 
                message_data = cz.read_msg(path_File, file_type) 
                all_users = message_data.get_all_users()

                return False, None

        except Exception as e:
            print(str(e))
            if str(e) == "'NoneType' object has no attribute 'get_all_users'":
                word = "File path is incorrect"
            else:
                word = "Dataset is not message dataset"
            return  True, word
    else:
        return False , None

######## direct for the datset page after adding message dataset
@app.callback(  Output('adding_message', 'href'),
            [  Input('upload-data_message', 'value'), Input('filepath_message', 'value')]
            )
def message_direct_datset(filename, filepath):
    try:
        path_File=filepath 
        file_part=filepath.split('\\')
        file_message = file_part[-1].split('.')
        file_type = file_message[-1]
        cz.read_msg(path_File, file_type) 
        message_data = cz.read_msg(path_File, file_type) 
        all_users = message_data.get_all_users()
        if (filename in added_message_name) or (path_File in all_message_path) or (filepath is None) or (filename is None) or (' ' in filename):
            return None
        else:
            href = '/Dataset'
            return href

    except Exception as e:
        # print(e)
        return None

######### set button n_clicks to zero
@app.callback(Output('adding_message', 'n_clicks'),
              [Input('upload-data_message', 'value'), Input('filepath_message', 'value')])
def adding_message_button(filename, filepath):
    if len(FilePath_message)>=1 and FilePath_message[-1]!=filepath:
        return None
    elif len(file_name_message)>=1 and file_name_message[-1]!=filename:
        return None


####### view all message data
@app.callback(Output('show_message_data', 'children'),
              [Input('view_message', 'n_clicks'), Input('close_message', 'n_clicks')
               ])
def view_message_data(n_clicks, click2):
    try:
        table = html.Div()
        if click2 is not None:
            return None

        if n_clicks is not None:
            message_record = update_message_data[-1][3]
            dict_list = []
            for record in message_record:
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
                html.Table(children=tab,
                        style={'border-collapse': 'collapse',
                                'border': '1px solid black',
                                'width': '100%'
                                })
            ])
            return table

    except Exception as e:
        print(e)


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
        try:
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
        
        except Exception as e:
            print(e)


connected_messageList = []
######## show connected users of specific user in message dataset
@app.callback(Output('show_connected_message_users', 'children'),
              [Input('connected_message_users', 'n_clicks'),
               Input('user_message', 'value')
               ])
def show_connected_message_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        connected_messageList.append(searchUser)
        try:
            message_data = update_message_data[-1][-1]
            all_users = update_message_data[-1][2]
            if searchUser is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif searchUser not in all_users:
                table=html.Div([
                    html.H5(children='User does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
                connected_users = message_data.get_connected_users(searchUser)
                if len(connected_users)==0:
                    table=html.Div([
                        html.H5(children='No connected users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
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

        except Exception as e:
            print(e)

###### set 0 n_clicks connected_message_users button
@app.callback(Output('connected_message_users', 'n_clicks'),
              [Input('user_message', 'value')])
def connected_message_users_button(user):
    if len(connected_messageList)>=1 and connected_messageList[-1]!=user:
        return None


message_record1 = []
message_record2 = []
####### show message records between 2 input users
@app.callback(Output('show_records_message_users', 'children'),
              [Input('message_user3', 'value'),
               Input('message_user2', 'value'),
               Input('record_message_users', 'n_clicks')
               ])
def between_message_users_records(user_1, user_2, click):
    table = html.Div()
    if click is not None:
        message_record1.append(user_1)
        message_record2.append(user_2)
        try:
            message_data = update_message_data[-1][-1]
            all_users = update_message_data[-1][2]
            if user_1 is None or user_2 is None:
                table=html.Div([
                    html.H5(children='Please enter number', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])            
            elif user_2 not in all_users:
                table=html.Div([
                    html.H5(children='User 1 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})]) 
            elif user_1 not in all_users:
                table=html.Div([
                    html.H5(children='User 2 does not exist', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
            else:
                dict_list = []
                for record in message_data.get_records(user_1, user_2):
                    dict_list.append(vars(record))
                if len(dict_list)==0:
                    table=html.Div([
                        html.H5(children='No records between two users', style={'color':'red', 'font-size': '20px', 'padding-left': '20px'})])
                else:
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

        except Exception as e:
            print(e)

###### set 0 n_clicks record_message_users button
@app.callback(Output('record_message_users', 'n_clicks'),
              [Input('message_user3', 'value'), Input('message_user2', 'value')])
def record_message_users_button(user1, user2):
    if len(message_record1)>=1 and message_record1[-1] != user1:
        return None
    elif len(message_record2)>=1 and message_record2[-1] != user2:
        return None


###### Visualize connection betwwen all users in message dataset
@app.callback(Output('show_visualize_message_connection', 'children'),
              [Input('visualize_message_connection', 'n_clicks')
               ])
def show_visualize_message_connection(n_clicks):
    try:
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

    except Exception as e:
        print(e)


######## return message file name to the next page
@app.callback( dash.dependencies.Output('file_name_message', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def file_name_message_nextpage(pathname): 
    file_message = pathname.split('/')
    for a in message_option:
        if len(file_message)>2 and file_message[2] == a[0]:
            for data in message_data_list:
                dataNew= data[0].split('.')
                if file_message[2]== dataNew[0]:
                    update_message_data.append(data)
            name = "Message Dataset :<%s>" % file_message[2]        
            return SimpleTitleBar(name)


######## get message option
@app.callback( dash.dependencies.Output('message_option', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def message_option_visu(pathname): 
    file_message = pathname.split('/')
    for a in message_option:
        if len(file_message)>2 and file_message[2] == a[0]:
            return a[1]


######## return message records card to the home page
@app.callback( dash.dependencies.Output('message_record_home', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def message_record_card_home(pathname):
    if len(message_data_list)>0 :
        message_data_name = []
        for x in message_data_list:
            a=x[0]
            record = len(x[3])
            link = '/Message_Dataset/'+str(a)
            message_data_name.append(DataSetCard(a, record, link))
        message_data_name.append(AddDataSetCard('message'))
        return message_data_name
    else:
        return AddDataSetCard('message')   

########### get message visualize option for navigation bar
@app.callback( dash.dependencies.Output('navbar_message_visu', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ]) 
def get_navbar_visu_message(pathname):
    path_set = pathname.split('/')
    if len(path_set)==4 and path_set[-3]== 'Message_Dataset':
        if path_set[-1]=='view_data':
            return SimpleTitleBar("Message Dataset :<%s> => All Data" % path_set[-2])
        elif path_set[-1]=='all_users':
            return SimpleTitleBar("Message Dataset :<%s> => All Users" % path_set[-2])
        elif path_set[-1]=='connected_users':
            return SimpleTitleBar("Message Dataset :<%s> => Connected Users" % path_set[-2])
        elif path_set[-1]== 'records_between_users':
            return SimpleTitleBar("Message Dataset :<%s> => Records Between Users" % path_set[-2])
        elif path_set[-1]== 'visualize_connection':
            return SimpleTitleBar("Message Dataset :<%s> => Visualize Connection" % path_set[-2])


######## return all message file names into message visualize sidebar
@app.callback( dash.dependencies.Output('message_data_visu_sidebar', 'children'),              
              [   dash.dependencies.Input('url', 'pathname')
            ]) 
def message_visu_sidebar(pathname):
    if len(message_data_list)>=1:
        output_message=[]
        for x in message_data_list:
            a=x[0]
            output_message.append(dcc.Link(a, href='/Message_Dataset/'+str(a)))
            output_message.append(html.Br())
        name_message=html.Div(children=output_message)
        return name_message 

# over message dataset
##################################################################################

@app.callback(dash.dependencies.Output('page-content', 'children'),
            [   dash.dependencies.Input('url', 'pathname')
            ])       
def display_page(pathname):
    try:
        path_set = pathname.split('/')
        if pathname=='/Call_Dataset':
            return call_dataset
        elif pathname=='/Cell_Dataset':
            return cell_dataset
        elif pathname=='/Message_Dataset':
            return message_dataset
        elif len(path_set)==3 and path_set[-2]== 'Call_Dataset':
            return call_dataset_file
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]=='view_data':
            return view_all_call_data
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]=='all_users':
            return get_all_users
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]=='connected_users':
            return connected_users  
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]== 'records_between_users':
            return  records_between_users
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]== 'close_contacts':
            return close_contacts
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]== 'ignored_call':
            return ignore_call_detail
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]== 'active_time':
            return active_time_user
        elif len(path_set)==4 and path_set[-3]== 'Call_Dataset' and path_set[-1]== 'visualize_connection':
            return visualize_connections
        elif len(path_set)==3 and  path_set[-2]== 'Cell_Dataset':
            return cell_dataset_file
        elif len(path_set)==4 and path_set[-3]== 'Cell_Dataset' and path_set[-1]=='view_cell_data':
            return view_all_cell_data
        elif len(path_set)==4 and path_set[-3]== 'Cell_Dataset' and path_set[-1]=='records_cell_id':
            return records_of_cell
        elif len(path_set)==4 and path_set[-3]== 'Cell_Dataset' and path_set[-1]=='population_around_cell':
            return population_around_cell
        elif len(path_set)==4 and path_set[-3]== 'Cell_Dataset' and path_set[-1]=='trip_visualize':
            return trip_visualize
        elif len(path_set)==3 and  path_set[-2]== 'Message_Dataset':
            return message_data_file
        elif len(path_set)==4 and path_set[-3]== 'Message_Dataset' and path_set[-1]=='view_data':
            return view_all_message_data
        elif len(path_set)==4 and path_set[-3]== 'Message_Dataset' and path_set[-1]=='all_users':
            return get_all_message_users
        elif len(path_set)==4 and path_set[-3]== 'Message_Dataset' and path_set[-1]=='connected_users':
            return connected_message_users  
        elif len(path_set)==4 and path_set[-3]== 'Message_Dataset' and path_set[-1]== 'records_between_users':
            return  message_records_between_users
        elif len(path_set)==4 and path_set[-3]== 'Message_Dataset' and path_set[-1]== 'visualize_connection':
            return visualize_message_connections
        elif pathname == '/Dataset':
            return index_page
        elif pathname=='/':
            return home_page
        else:
            return home_page
    except Exception as e:
            print(str(e))

if __name__ == '__main__':
    app.run_server(debug=True)
