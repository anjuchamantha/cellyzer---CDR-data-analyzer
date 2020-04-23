import base64
import datetime
import io
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import folium
import flask
import pandas as pd
import os
import sys

sys.path.insert(0, '../')
import cellyzer as cz

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])
server = app.server

app.config.suppress_callback_exceptions = True

image_filename = 'cdr.jpg'
encoded_mage = base64.b64encode(open(image_filename, 'rb').read())

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem 1rem 1rem",
    "background-color": "#f8f9fa",
}

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


## Front page
index_page = html.Div([
    html.H1(className='index_page_CELLYZER',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='index_page_Dashboard',
                children='Dashboard'
                ),

        html.Hr(className='horizontal-lines'),
        html.Div(
            [
                dbc.Button(
                    "Add a Dataset",
                    id="collapse-button",
                    className="dashboard-button",
                    color="dark",
                ),
                dbc.Collapse(
                    html.Div(
                        [
                            dcc.Link('Call Dataset', href='/Call_Dataset'),
                            html.Br(),
                            dcc.Link('Cell Dataset', href='/Cell_Dataset'),
                            html.Br(),
                            dcc.Link('Message Dataset', href='/Message_Dataset')
                        ],
                        className='index_page_dataset_div'
                    ),
                    id="collapse",
                ),
            ],
        ),
    ],
        className='index_page_Dashboard_div'
    ),
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
            className='index_page_welcome_div'
        )
    ])
],
    className='index_page_div'
)


@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# over front page

#######################################################################
## page for call dataset
call_dataset = html.Div([
    dcc.Location(id='url_dataset', refresh=False),
    html.Div(id='page-dataset')
])

index_dataset = html.Div([
    html.H1(className='index_dataset_CELLYZER',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='index_dataset_Dasboard',
                children='Dashboard'
                ),
        html.Hr(className='horizontal-lines'),
        html.Div([
            html.H5("Call Dataset"),
            html.Div(id='call-data')
        ], className='index_dataset_Call_Dataset',
        )
    ],
        className='index_dataset_Dashboard_div',
    ),
    html.Div([
        html.Div([
            dbc.Alert("ADD  CALL  DATASET", color="dark"),
        ],
            className='index_dataset_add_call_data_div'
        ),
    ]),
    dbc.FormGroup(
        [
            dbc.Label("File Path", html_for="example-email-row", width=2),
            dbc.Col(
                dbc.Input(
                    type="input", id="filepath", placeholder="Enter File Path",
                    style={'width': '500px', 'border': '1px solid black'}
                ),
                width=10,
            ),
        ],
        row=True,
        style={
            'padding-left': '30px',
        }
    ),
    html.P('Enter correct path of adding file', style={
        'padding-left': '30px'
    }),
    html.Br(),
    dbc.FormGroup(
        [
            dbc.Label("File Types", html_for="example-radios-row", width=2),
            dbc.Col(
                dbc.RadioItems(
                    id="example-radios-row",
                    options=[
                        {"label": "CSV", "value": 1},
                        {"label": "XLSX", "value": 2},
                        {"label": "JSON", "value": 3},
                    ],
                ),
                width=10,
            ),
        ],
        row=True,
        style={
            'padding-left': '30px'
        }
    ),
    dcc.Upload(id='upload-data_call',
               children=html.Div([
                   html.Button('ADD CALL DATA', className='index_datatset_calldata_button'
                               )
               ]),
               className='index_dataset_upload_data',
               # Allow multiple files to be uploaded
               multiple=True
               ),
    # html.Div([
    #     html.H3(
    #     children='Map Visualization',
    #     style={
    #         # 'textAlign': 'center',
    #         'color': 'orange',
    #         'background': 'black',
    #         'padding-top': '20px',
    #         'padding-bottom': '20px',
    #         'width': '350px',
    #         'padding-left': '90px'
    #     }),
    #     html.Div([
    #         html.H6('Longitude:'),
    #         dcc.Input(id="long", type='text', placeholder='Longitude')

    #     ]),
    #     html.Div([
    #         html.H6('Latitude:'),
    #         dcc.Input(id="lat", type='text', step='any', placeholder='Latitude')

    #     ]),
    #     html.Div([
    #         html.Button(id='submit_but', type='submit', children='Submit',
    #         style={
    #             'background-color': '#4CAF50',
    #             'color': 'white',
    #             'border': 'none',
    #             'font-size': '15px',

    #         })
    #     ],
    #     style={
    #         'margin-top': '20px',
    #         'margin-bottom': '20px',
    #         'padding-left': '20px'
    #     }) ,
    #     html.Iframe(id='map_new',
    #     style={
    #         'width': '100%',
    #         'height': '500px'
    #     }
    # )
    # ])
],
    className='index_dataset_div'
)

sample_call_data = html.Div([
    dcc.Location(id='url_sample_call_data', refresh=False),
    html.Div(id='page_sample_call_data') 
])

call_dataset_file= html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([html.H5("Call Dataset")], className='index_dataset_Call_Dataset')  
    ],
    className='sample_dataset_Dashboard_div'),
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

view_all_call_data = html.Div([
    html.H1(className='sample_call_data_cellyzer',children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([html.H5("Call Dataset")], className='index_dataset_Call_Dataset'),
        html.Div([html.H6("All Data")], className='index_page_dataset_div_all_user')     
    ],
    className='sample_dataset_Dashboard_div' 
    ), 
    html.Div([
        html.Div([
            html.H4('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')], 
        className='index_dataset_add_call_data_div'),         
    ]), 
    html.Div([
        html.H4(children='Get All Data', className='sample_call_visualize_all_user')], 
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
    ),
    html.Div([
        html.Button('VIEW DATA', id='view', className='sample_call_dataset_viewdata'),
        html.Button('CLOSED DATA', id='close', className='sample_call_dataset_close')],
        className='sample_call_dataset_view_div'),
    html.Div(id='show_data', className='sample_call_dataset_show'),
    ],
    className='sample_call_dataset_div')

######## page for get all users
get_all_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard',children='Dashboard'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'),
        html.Div([html.H6("All Users")], className='index_page_dataset_div_all_user')  
    ],
    className='sample_dataset_Dashboard_div' 
    ),   
    html.Div([
        html.Div([
            html.H3('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')], 
            className='index_dataset_add_call_data_div')         
    ]), 
    html.Div([
        html.H4(children='Get All Users', className='sample_call_visualize_all_user')], 
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
    ),
    html.Div([
        html.Button('Get All Users', id='get_users', className='sample_call_dataset_viewdata')],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_all_users', className='sample_call_dataset_show_all_users'), 
    ],
    className='sample_call_dataset_div')

####### page for show connected users of specific user
connected_users = html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([html.H5("Call Dataset")], className='index_page_dataset_div'), 
        html.Div([html.H6("Connected Users")], className='index_page_dataset_div_all_user')   
    ], 
    className='sample_dataset_Dashboard_div' 
    ), 
    html.Div([
        html.Div([
            html.H4('CALL  DATASET  VISUALIZATION', className='index_dataset_add_call_data')], 
            className='index_dataset_add_call_data_div'),         
    ]), 
    html.Div([
        html.H3(children='Connected Users Of Specific User', className='sample_call_visualize_all_user')], 
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
    ),
    html.Div([
        html.H6('Enter Specific User Number:'),
        dcc.Input(id="search", type='text', placeholder='Enter number'),
        html.Br(),
        html.Br(),
        html.Button('Connected Users', id='connected_users', className='sample_call_dataset_viewdata')], 
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        print(filename)
        filename = filename[0]
        path_File = os.path.join(filepath, filename)
        call_data_list.append([filename, path_File])
        print(path_File)
        output_call = []
        for x in call_data_list:
            a = x[0].split('.')
            output_call.append(dcc.Link(a[0], href='/Call_Dataset/' + str(a[0])))
            output_call.append(html.Br())
            # output_call.append(dcc.Link(a[0], href='/Call_Dataset/'+str(a[0]), id='link'))
        name = html.Div(
            children=output_call
        )
        return name

    except Exception as e:
        print(e)


@app.callback(dash.dependencies.Output('page_sample_call_data', 'children'),
            [   dash.dependencies.Input('url_sample_call_data', 'pathname')
            ])   
def display_sample_call_data(pathname):
    if pathname=='/Call_Dataset/view_data':
        return view_all_call_data
    elif pathname=='/Call_Dataset/all_users':
        return get_all_users
    elif pathname=='/Call_Dataset/connected_users':
        return connected_users  
    elif pathname== '/Call_Dataset/records_between_users':
        return  records_between_users
    elif pathname== '/Call_Dataset/close_contacts':
        return close_contacts
    elif pathname== '/Call_Dataset/ignored_call':
        return ignore_call_detail
    elif pathname== '/Call_Dataset/active_time':
        return active_time_user
    elif pathname== '/Call_Dataset/visualize_connection':
        return visualize_connections
    else:
        return call_dataset_file


@app.callback(dash.dependencies.Output('page-dataset', 'children'),
              [dash.dependencies.Input('url_dataset', 'pathname')
               ])
def display_sample_data(pathname):
    filename = str(pathname).split('/')
    if filename[-2] == 'Call_Dataset':
        return sample_call_data
    else:
        return index_dataset

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
        c=cz.read_call(filepath)
        dict_list = []
        for record in c.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab=[]
        column=[]
        for i in header:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        count=0
        for j in dict_list:
            value=list(j.values())
            count+=1       
            row_content=[]
            if count>100:
                break
            row_content=[]
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.H2(filename),
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
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
            [   Input('get_users', 'n_clicks')
            ])
def show_all_users(n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        all_users= call_data.get_all_users()
        tab=[]
        column=[]
        column.append(html.Th('Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        for user in all_users:
            row_content=[]   
            row_content.append(html.Td(user ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '200px'
                })
        ])
        return table

######## show cnnected users of specific user
@app.callback(Output('show_connected_users', 'children'),
            [   Input('connected_users', 'n_clicks'),
                Input('search', 'value')
            ])
def show_connected_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        connected_users= call_data.get_connected_users(searchUser)
        tab=[]
        column=[]
        column.append(html.Th('Connected Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        for user in connected_users:
            row_content=[]   
            row_content.append(html.Td(user ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '200px'
                })
        ])
        return table

####### show records between 2 input users
@app.callback(Output('show_records_users', 'children'),
            [   Input('search_3', 'value'), 
                Input('search_2', 'value'), 
                Input('record_users', 'n_clicks')
            ])
def between_users_records(user_1,user_2, click):
    table = html.Div()

    if click is not None:
        filepath = call_data_list[0][1]
        c=cz.read_call(filepath)
        dict_list = []
        for record in c.get_records(user_1, user_2):
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab=[]
        column=[]
        for i in header:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        count=0
        for j in dict_list:
            value=list(j.values())
            count+=1       
            row_content=[]
            if count>100:
                break
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '100%'
                })
        ])
        return table

######## show close contacts
@app.callback(Output('show_close_contact', 'children'),
            [   Input('user_3', 'value'),
                Input('contact', 'value'),
                Input('close_contacts', 'n_clicks')
            ])
def show_close_contatcs(user_3, contact, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        connected_users= call_data.get_close_contacts(user_3, contact)
        tab=[]
        column=[]
        col1=html.Th("Contact No.", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col1)
        col2=html.Th("No of interactions between users", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        numbers=list(connected_users.keys())
        NoContacts=list(connected_users.values())
        for j in range(len(numbers)):
            row_content=[]
            row_content.append(html.Td(numbers[j] ,style={'border': '1px solid black', 'padding-left':'10px'}))
            row_content.append(html.Td(str(NoContacts[j]) ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '50%'
                })
        ])
        return table

######## show most active time
@app.callback(Output('show_active_time', 'figure'),
            [   Input('active_time', 'n_clicks'),
                Input('user_4', 'value')
            ])
def show_active_time(n_clicks, user_4):
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        active_time= call_data.get_most_active_time(user_4)
        return cz.visualization.active_time_bar_chart(active_time)

######### Show ignored call
@app.callback(Output('show_ignore_call', 'children'),
            [   Input('user_5', 'value'),
                Input('ignore_call', 'n_clicks')
            ])
def show_ignore_call(user_5, n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        ignore_call= call_data.get_ignored_call_details(user_5)

        key=list(ignore_call[0].keys())
        tab=[]
        column=[]
        for i in key:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        for j in ignore_call:
            value=list(j.values())
            row_content=[]
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '100%'
                })
        ])
        return table

###### Visualize connection betwwen all users
@app.callback(Output('show_visualize_connection', 'children'),
            [   Input('visualize_connection', 'n_clicks')
            ])
def show_visualize_connection(n_clicks):
    if n_clicks is not None:
        filepath = call_data_list[0][1]
        call_data=cz.read_call(filepath)
        visu_conn= call_data.visualize_connection_network()
        tab=[]
        column=[]
        col1=html.Th("User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col1)
        col2=html.Th("Connected User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        for connection in visu_conn[0]:
            row_content=[]
            row_content.append(html.Td(connection[0] ,style={'border': '1px solid black', 'padding-left':'10px'}))
            row_content.append(html.Td(connection[1] ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '50%'
                })
        ])
        return table
##############################################################
## Page for cell dataset

cell_dataset = html.Div([
    dcc.Location(id='url_cell_dataset', refresh=False),
    html.Div(id='page_cell_dataset')
])

index_cell_dataset = html.Div([
    html.H1(className='index_cell_dataset_cellyzer',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='index_cell_dataset_Dashboard',
                children='Dashboard'
                ),
        html.Hr(),
        html.Div([
            html.H5("Cell Dataset"),
            html.Div(id='cell-data')
        ],
            className='index_cell_dataset_h5'
        )
    ],
        className='index_cell_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.Div([
                dbc.Alert("ADD  CELL  DATASET", color="dark"),
            ],
                className='index_dataset_add_call_data_div'
            ),
        ]),
        dbc.FormGroup(
            [
                dbc.Label("File Path", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="input", id="filepath_cell", placeholder="Enter File Path",
                        style={'width': '500px', 'border': '1px solid black'}
                    ),
                    width=10,
                ),
            ],
            row=True,
            style={
                'padding-left': '30px',
            }
        ),
        html.P('Enter correct path of adding file', style={
            'padding-left': '30px'
        }),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("File Types", html_for="example-radios-row", width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="example-radios-row",
                        options=[
                            {"label": "CSV", "value": 1},
                            {"label": "XLSX", "value": 2},
                            {"label": "JSON", "value": 3},
                        ],
                    ),
                    width=10,
                ),
            ],
            row=True,
            style={
                'padding-left': '30px'
            }
        ),
    ]),
    dcc.Upload(id='upload-data_cell',
               children=html.Div([
                   html.Button('ADD CELL DATA', className='index_celldata_add_button'
                               )
               ]),
               className='index_cell_dataset_upload_data',
               # Allow multiple files to be uploaded
               multiple=True
               ),
],
    className='index_cell_dataset_div'
)


sample_cell_data = html.Div([
    dcc.Location(id='url_sample_cell_data', refresh=False),
    html.Div(id='page_sample_cell_data') 
])

cell_dataset_file= html.Div([
    html.H1(className='sample_cell_data_cellyzer', children='CELLYZER' ),
    html.Div([
        html.H2(className='sample_cell_dataset_Dashboard', children='Dashboard'),
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
    html.H1(className='sample_call_data_cellyzer',children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        filename=filename[0]
        path_File=os.path.join(filepath, filename)
        cell_data_list.append([filename, path_File])
        output_cell=[]
        for x in cell_data_list:
            a=x[0].split('.')
            output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/'+str(a[0])))
            output_cell.append(html.Br())
        name_cell=html.Div(
            children=output_cell
            )
        return name_cell

    except Exception as e:
        print(e)

@app.callback(dash.dependencies.Output('page_cell_dataset', 'children'),
            [   dash.dependencies.Input('url_cell_dataset', 'pathname')
            ])   
def display_sample_cell_data(pathname):
    filename=str(pathname).split('/')
    if filename[-2]=='Cell_Dataset':
        return sample_cell_data
    elif pathname=='/':
        return index_page
    else:
        return index_cell_dataset

###### read cell data
@app.callback(Output('show_cell_data', 'children'),
            [   Input('view_cell', 'n_clicks'), Input('close_cell', 'n_clicks')
            ])
def view_cell_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        call_data=cz.read_call(filepath_call)
        split_name= filename.split('.')
        file_type=split_name[-1]
        c=cz.read_cell(filepath,filepath_call, call_data, file_type)
        dict_list = []
        for record in c.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab=[]
        column=[]
        for i in header:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        count=0
        for j in dict_list:
            value=list(j.values())
            count+=1       
            row_content=[]
            if count>100:
                break
            row_content=[]
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.H2(filename),
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '100%'
                })
        ])
        return table

@app.callback(Output('close_cell', 'n_clicks'),
            [   Input('view_cell', 'n_clicks')
            ])
def close_cell_data(n_clicks):
    if n_clicks is not None:
        return None

###### get cell_id records
@app.callback(Output('show_records_cell', 'children'),
            [   Input('records_cell', 'n_clicks'),
                Input('cell_id', 'value')
            ])
def get_cell_records(n_clicks, cell_id):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        call_data=cz.read_call(filepath_call)
        split_name= filename.split('.')
        file_type=split_name[-1]
        antana_dataset=cz.read_cell(filepath,filepath_call, call_data, file_type)
        record_cell=antana_dataset.get_cell_records(cell_id)
        cell=record_cell.get_cell_id()
        print(record_cell)
        return html.H5('Cell_id: '+cell, className='index_dataset_add_call_data')


######## get population around cell
@app.callback(Output('show_population', 'children'),
            [   Input('population_button', 'n_clicks'),
            ])
def get_population(n_clicks):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        call_data=cz.read_call(filepath_call)
        split_name= filename.split('.')
        file_type=split_name[-1]
        antana_dataset=cz.read_cell(filepath,filepath_call, call_data, file_type)
        population= antana_dataset.get_population()
        return cz.visualization.cell_population_visualization(population)

######### get trip visualize
@app.callback(Output('show_trip_visualize', 'children'),
            [   Input('trip_user', 'value'),
                Input('trip_visualize_button', 'n_clicks')
            ])
def trip_visualization(user, n_clicks):
    if n_clicks is not None:
        filepath = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        filepath_call = call_data_list[0][1]
        call_data=cz.read_call(filepath_call)
        split_name= filename.split('.')
        file_type=split_name[-1]
        antana_dataset=cz.read_cell(filepath,filepath_call, call_data, file_type)
        trip_visualize=antana_dataset.get_trip_details(user)
        return cz.visualization.trip_visualization(trip_visualize)

######## get page after click link
@app.callback(dash.dependencies.Output('page_sample_cell_data', 'children'),
            [   dash.dependencies.Input('url_sample_cell_data', 'pathname')
            ])   
def display_cell_link(pathname):
    if pathname=='/Cell_Dataset/view_cell_data':
        return view_all_cell_data
    elif pathname=="/Cell_Dataset/records_cell_id":
        return records_of_cell
    elif pathname== '/Cell_Dataset/population_around_cell':
        return population_around_cell
    elif pathname== '/Cell_Dataset/trip_visualize':
        return trip_visualize
    else:
        return cell_dataset_file


# over cell
###########################################################################
## Page for message dataset

message_dataset = html.Div([
    dcc.Location(id='url_message_dataset', refresh=False),
    html.Div(id='page_message_dataset')
])

index_message_dataset = html.Div([
    html.H1(className='index_message_dataset_cellyzer',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='index_message_dataset_Dashboard',
                children='Dashboard'
                ),
        html.Hr(),
        html.Div([
            html.H5("Message Dataset"),
            html.Div(id='message-data')
        ],
            className='index_message_dataset_h5'
        )
    ],
        className='index_message_dataset_Dashboard_div'
    ),
    html.Div([
        html.Div([
            html.Div([
                dbc.Alert("ADD  MESSAGE  DATASET", color="dark"),
            ],
                className='index_dataset_add_call_data_div'
            ),
        ]),
        dbc.FormGroup(
            [
                dbc.Label("File Path", html_for="example-email-row", width=2),
                dbc.Col(
                    dbc.Input(
                        type="input", id="filepath_message", placeholder="Enter File Path",
                        style={'width': '500px', 'border': '1px solid black'}
                    ),
                    width=10,
                ),
            ],
            row=True,
            style={
                'padding-left': '30px',
            }
        ),
        html.P('Enter correct path of adding file', style={
            'padding-left': '30px'
        }),
        html.Br(),
        dbc.FormGroup(
            [
                dbc.Label("File Types", html_for="example-radios-row", width=2),
                dbc.Col(
                    dbc.RadioItems(
                        id="example-radios-row",
                        options=[
                            {"label": "CSV", "value": 1},
                            {"label": "XLSX", "value": 2},
                            {"label": "JSON", "value": 3},
                        ],
                    ),
                    width=10,
                ),
            ],
            row=True,
            style={
                'padding-left': '30px'
            }
        ),
    ]),
    dcc.Upload(id='upload-data_message',
               children=html.Div([
                   html.Button('ADD MESSAGE DATA', className='index_messagedata_add_button'
                               )
               ]),
               className='index_message_dataset_upload_data',
               # Allow multiple files to be uploaded
               multiple=True
               )],
    className='index_message_dataset_div'
)


sample_message_data = html.Div([
    dcc.Location(id='url_sample_message_data', refresh=False),
    html.Div(id='page_sample_message_data') 
])

message_data_file= html.Div([
    html.H1(className='sample_call_data_cellyzer', children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
        html.Div([html.H5("Message Dataset")], className='index_dataset_Call_Dataset') ,
        html.Div([dcc.Link("Home", href='/')], className='index_page_dataset_div'), 
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
    html.H1(className='sample_call_data_cellyzer',children='CELLYZER'),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard', children='Dashboard'),
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        html.H2(className='sample_call_dataset_Dashboard',children='Dashboard'),
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
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
        style={'padding-left': '30px', 'margin-top':'40px', 'margin-bottom':'20px'}
    ), 
    html.Div([
        html.Button('Visualize Connection', id='visualize_message_connection', className='sample_call_dataset_viewdata')], 
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
        filename=filename[0]
        path_File=os.path.join(filepath, filename)
        message_data_list.append([filename, path_File])
        output_message=[]
        for x in message_data_list:
            a=x[0].split('.')
            output_message.append(dcc.Link(a[0], href='/Message_Dataset/'+str(a[0])))
            output_message.append(html.Br())
        name_message=html.Div(
            children=output_message
            )
        return name_message

    except Exception as e:
        print(e)

@app.callback(dash.dependencies.Output('page_message_dataset', 'children'),
            [   dash.dependencies.Input('url_message_dataset', 'pathname')
            ])   
def display_sample_message_data(pathname):
    filename=str(pathname).split('/')
    if filename[-2]=='Message_Dataset':
        return sample_message_data
    else:
        return index_message_dataset

@app.callback(dash.dependencies.Output('page_sample_message_data', 'children'),
            [   dash.dependencies.Input('url_sample_message_data', 'pathname')
            ])   
def display_sample_message_data_file(pathname):
    if pathname=='/Message_Dataset/view_data':
        return view_all_message_data
    elif pathname=='/Message_Dataset/all_users':
        return get_all_message_users
    elif pathname=='/Message_Dataset/connected_users':
        return connected_message_users  
    elif pathname== '/Message_Dataset/records_between_users':
        return  message_records_between_users
    elif pathname== '/Message_Dataset/visualize_connection':
        return visualize_message_connections
    else:
        return message_data_file

####### view all message data
@app.callback(Output('show_message_data', 'children'),
            [   Input('view_message', 'n_clicks'), Input('close_message', 'n_clicks')
            ])
def view_message_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name= filename_message.split('.')
        file_type=split_name[-1]
        message_data=cz.read_msg(filepath_message, file_type)
        dict_list = []
        for record in message_data.get_records():
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab=[]
        column=[]
        for i in header:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        count=0
        for j in dict_list:
            value=list(j.values())
            count+=1       
            row_content=[]
            if count>100:
                break
            row_content=[]
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.H2(filename_message),
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '100%'
                })
        ])
        return table

########## set button value
@app.callback(Output('close_message', 'n_clicks'),
            [   Input('view_message', 'n_clicks')
            ])
def close_message_data(n_clicks):
    if n_clicks is not None:
        return None

########## show all message users
@app.callback(Output('show_all_message_users', 'children'),
            [   Input('get_message_users', 'n_clicks')
            ])
def show_all_message_users(n_clicks):
    table = html.Div()
    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name= filename_message.split('.')
        file_type=split_name[-1]
        message_data=cz.read_msg(filepath_message, file_type)
        all_users= message_data.get_all_users()
        tab=[]
        column=[]
        column.append(html.Th('Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        for user in all_users:
            row_content=[]   
            row_content.append(html.Td(user ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '200px'
                })
        ])
        return table

######## show cnnected users of specific user in message dataset
@app.callback(Output('show_connected_message_users', 'children'),
            [   Input('connected_message_users', 'n_clicks'),
                Input('user_message', 'value')
            ])
def show_connected_message_users(n_clicks, searchUser):
    table = html.Div()
    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name= filename_message.split('.')
        file_type=split_name[-1]
        message_data=cz.read_msg(filepath_message, file_type)
        connected_users= message_data.get_connected_users(searchUser)
        tab=[]
        column=[]
        column.append(html.Th('Connected Users', style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        for user in connected_users:
            row_content=[]   
            row_content.append(html.Td(user ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '200px'
                })
        ])
        return table

####### show message records between 2 input users
@app.callback(Output('show_records_message_users', 'children'),
            [   Input('message_user3', 'value'), 
                Input('message_user2', 'value'), 
                Input('record_message_users', 'n_clicks')
            ])
def between_message_users_records(user_1, user_2, click):
    table = html.Div()

    if click is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name= filename_message.split('.')
        file_type=split_name[-1]
        message_data=cz.read_msg(filepath_message, file_type)
        dict_list = []
        for record in message_data.get_records(user_1, user_2):
            dict_list.append(vars(record))
        header = list(dict_list[0].keys())
        tab=[]
        column=[]
        for i in header:
            column.append(html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'}))
        tab.append(html.Tr(children=column))
        count=0
        for j in dict_list:
            value=list(j.values())
            count+=1       
            row_content=[]
            if count>100:
                break
            for x in value:
                row_content.append(html.Td(x ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '100%'
                })
        ])
        return table

###### Visualize connection betwwen all users in message dataset
@app.callback(Output('show_visualize_message_connection', 'children'),
            [   Input('visualize_message_connection', 'n_clicks')
            ])
def show_visualize_message_connection(n_clicks):
    table = html.Div()

    if n_clicks is not None:
        filename_message = message_data_list[0][0]
        filepath_message = message_data_list[0][1]
        split_name= filename_message.split('.')
        file_type=split_name[-1]
        message_data=cz.read_msg(filepath_message, file_type)
        visu_conn= message_data.visualize_connection_network()
        tab=[]
        column=[]
        col1=html.Th("User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col1)
        col2=html.Th("Connected User", style={'border': '1px solid black', 'background-color': '#4CAF50', 'color':'white'})
        column.append(col2)
        tab.append(html.Tr(children=column))
        for connection in visu_conn[0]:
            row_content=[]
            row_content.append(html.Td(connection[0] ,style={'border': '1px solid black', 'padding-left':'10px'}))
            row_content.append(html.Td(connection[1] ,style={'border': '1px solid black', 'padding-left':'10px'}))
            tab.append(html.Tr(children=row_content, style={'height': '5px'}))
        table=html.Div([
            html.Table(children=tab, 
                style={'border-collapse':'collapse',
                    'border': '1px solid black',
                    'width': '50%'
                })
        ])
        return table


# over message dataset



######### link for front page 
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
    else:
        return index_page


# @app.callback(dash.dependencies.Output('file_name', 'children') ,
#     [   
#     ])   
# def show_name():
#     file_name=call_data_list[0][0].split('.')
#     print(file_name)
#     return file_name[0]
# def show_f():
#     c=str(flask.request.full_path)
#     c1=c.split('/')
#     return c1[-1]
# def show_name(href, n_clicks):
#     if n_clicks is not None:
#         filename=str(href).split('/')
#         new_name=filename[-1]
#         print(new_name)
#         return new_name

if __name__ == '__main__':
    app.run_server(debug=True)
