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


def parse_data(contents, filename):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        # elif 'txt' or 'tsv' in filename:
        #     # Assume that the user upl, delimiter = r'\s+'oaded an excel file
        #     df = pd.read_csv(
        #         io.StringIO(decoded.decode('utf-8')), delimiter = r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df


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
    html.H1(className='sample_call_data_cellyzer',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='sample_call_dataset_Dashboard',
                children='Dashboard'
                ),
        html.Div([
            html.H5("Call Dataset"),
            # html.Div(id='call-data')
        ],
            className='sample_call_dataset_h5'
        )
    ],
        className='sample_dataset_Dashboard_div'
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view', className='sample_call_dataset_viewdata'
                    ),
        html.Button('CLOSED DATA', id='close', className='sample_call_dataset_close'
                    )],
        className='sample_call_dataset_view_div'
    ),
    html.Div(id='show_data', className='sample_call_dataset_show'
             )],
    className='sample_call_dataset_div'
)
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


@app.callback(dash.dependencies.Output('page-dataset', 'children'),
              [dash.dependencies.Input('url_dataset', 'pathname')
               ])
def display_sample_data(pathname):
    filename = str(pathname).split('/')
    if filename[-2] == 'Call_Dataset':
        return sample_call_data
    else:
        return index_dataset


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
        c = cz.read_csv(filepath)
        d = c.get_records()
        key = list(d[0].keys())
        tab = []
        column = []
        for i in key:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for j in d:
            value = list(j.values())
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


@app.callback(Output('close', 'n_clicks'),
              [Input('view', 'n_clicks')
               ])
def close_data(n_clicks):
    if n_clicks is not None:
        return None


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
    html.H1(className='sample_cell_data_cellyzer',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='sample_cell_dataset_Dashboard',
                children='Dashboard'
                ),
        html.Div([
            html.H5("Cell Dataset")
        ],
            className='sample_cell_dataset_h5'
        )
    ],
        className='sample_cell_dataset_Dashboard_div'
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view_cell', className='sample_cell_dataset_viewdata'
                    ),
        html.Button('CLOSED DATA', id='close_cell', className='sample_cell_dataset_close'
                    )],
        className='sample_cell_dataset_view_div'
    ),
    html.Div(id='show_cell_data',
             className='sample_cell_dataset_show'
             )
],
    className='sample_cell_dataset_div'
)

cell_data_list = []


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
            output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/' + str(a[0])))
            output_cell.append(html.Br())
        name_cell = html.Div(
            children=output_cell
        )
        return name_cell

    except Exception as e:
        print(e)


@app.callback(dash.dependencies.Output('page_cell_dataset', 'children'),
              [dash.dependencies.Input('url_cell_dataset', 'pathname')
               ])
def display_sample_cell_data(pathname):
    filename = str(pathname).split('/')
    if filename[-2] == 'Cell_Dataset':
        return sample_cell_data
    else:
        return index_cell_dataset


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
        c = cz.read_csv(filepath)
        d = c.get_records()
        key = list(d[0].keys())
        tab = []
        column = []
        for i in key:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for j in d:
            value = list(j.values())
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
    html.H1(className='sample_message_data_cellyzer',
            children='CELLYZER'
            ),
    html.Div([
        html.H2(className='sample_message_dataset_Dashboard',
                children='Dashboard'
                ),
        html.Div([
            html.H5("Message Dataset")
        ],
            className='sample_message_dataset_h5'
        )
    ],
        className='sample_message_dataset_Dashboard_div'
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view_message', className='sample_message_dataset_viewdata'
                    ),
        html.Button('CLOSED DATA', id='close_message', className='sample_message_dataset_close'
                    )],
        className='sample_message_dataset_view_div'
    ),
    html.Div(id='show_message_data',
             className='sample_message_dataset_show'
             )
],
    className='sample_message_dataset_div'
)

message_data_list = []


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
            output_message.append(dcc.Link(a[0], href='/Message_Dataset/' + str(a[0])))
            output_message.append(html.Br())
        name_message = html.Div(
            children=output_message
        )
        return name_message

    except Exception as e:
        print(e)


@app.callback(dash.dependencies.Output('page_message_dataset', 'children'),
              [dash.dependencies.Input('url_message_dataset', 'pathname')
               ])
def display_sample_message_data(pathname):
    filename = str(pathname).split('/')
    if filename[-2] == 'Message_Dataset':
        return sample_message_data
    else:
        return index_message_dataset


@app.callback(Output('show_message_data', 'children'),
              [Input('view_message', 'n_clicks'), Input('close_message', 'n_clicks')
               ])
def view_message_data(n_clicks, click2):
    table = html.Div()
    if click2 is not None:
        return None

    if n_clicks is not None:
        filepath = message_data_list[0][1]
        filename = message_data_list[0][0]
        c = cz.read_csv(filepath)
        d = c.get_records()
        key = list(d[0].keys())
        tab = []
        column = []
        for i in key:
            column.append(
                html.Th(i, style={'border': '1px solid black', 'background-color': '#4CAF50', 'color': 'white'}))
        tab.append(html.Tr(children=column))
        for j in d:
            value = list(j.values())
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


@app.callback(Output('close_message', 'n_clicks'),
              [Input('view_message', 'n_clicks')
               ])
def close_message_data(n_clicks):
    if n_clicks is not None:
        return None


# over message dataset

@app.callback(dash.dependencies.Output('map_new', 'srcDoc'),
              [dash.dependencies.Input('long', 'value'),
               dash.dependencies.Input('lat', 'value'),
               dash.dependencies.Input('submit_but', 'n_clicks')
               ])
def show_map(longitude, latitude, clicks):
    try:
        if clicks is not None:
            mapit = folium.Map(location=[float(longitude), float(latitude)], zoom_start=12)
            folium.Marker([longitude, latitude], popup='<strong>Location One</strong>').add_to(mapit)
            mapit.save('mapi.html')

            return open('mapi.html', 'r').read()
        # map_hooray = folium.Map(location=[longitude, latitude], zoom_start=12)
        # return map_hooray
    except ValueError:
        print("Not a float")


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
