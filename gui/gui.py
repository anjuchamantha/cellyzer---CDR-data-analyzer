import base64
import datetime
import io
import plotly.graph_objs as go
# import cufflinks as cf
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import folium
import flask
import pandas as pd
import dash_bootstrap_components as dbc


external_stylesheets = [{'external_url': 'https://stackpath.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min'
                                         '.css'}]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets])
server = app.server

app.config.suppress_callback_exceptions = True

# colors = {
#     "graphBackground": "#F5F5F5",
#     "background": "#ffffff",
#     "text": "#000000"
# }
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
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'black',
                'padding-left': '20px'
            }
        ),
        html.Hr(style={'color': 'white'}),
        html.Div(
            [
                dbc.Button(
                    "ADD A DATASET",
                    id="collapse-button",
                    className="mb-3",
                    color="dark",
                    style={'margin-left': '1rem'}
                ),
                dbc.Collapse(
                    html.Div([
                        dcc.Link('Call Dataset', href='/Call_Dataset'),
                        html.Br(),
                        dcc.Link('Cell Dataset', href='/Cell_Dataset'),
                        html.Br(),
                        dcc.Link('Message Dataset', href='/Message_Dataset')
                    ],
                        style={
                            'padding': '6px 8px 6px 20px',
                            'text-decration': 'none',
                            'color': 'orange',
                            'display': 'block',
                            'border': '1px solid black'
                        }
                    ),
                    id="collapse",
                ),
            ]
        ),

    ],
        style=SIDEBAR_STYLE
    ),
    html.Div([
        html.Div([
            html.Img(
                src='data:image/jpg;base64,{}'.format(encoded_mage.decode()),
                style={
                    'width': '100%',
                    'height': '500px'
                }),
            html.Div([
                html.H1("WELCOME"),
                html.H1('CDR DATA ANALYSIS')
            ],
                style={
                    'position': 'fixed',
                    'bottom': '200px',
                    'background': 'rgb(0,0,0)',
                    'background': 'rgb(0,0,0, 0.5)',
                    'color': 'orange',
                    'width': '80%',
                    'textAlign': 'center',
                    'font-weight': '900',
                    'font-size': '20px'
                })
        ],
            style={
                'max-width': '1300px',
                'margin': '0 0'
            })
    ])
],
    style={
        'margin-left': '16rem',
        'padding': '0px 10px'
    }
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
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Call Dataset"),
            html.Div(id='call-data')
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.Div([
            html.H3('ADD  CALL  DATASET',
                    style={
                        'background': 'gray',
                        'padding-top': '10px',
                        'padding-bottom': '10px',
                        'padding-left': '50px',
                        'color': 'white'
                    })
        ],
            style={
                'width': '700px',
                'margin-top': '50px',
                'padding-left': '30px'
                # 'position':'fixed'
            }),
    ]),
    dcc.Upload(
        id='upload-data_call',
        children=html.Div([
            html.Button('ADD CALL DATA',
                        style={
                            'background-color': '#4CAF50',
                            'height': '50px',
                            'border': 'none',
                            'color': 'white',
                            'text-align': 'center',
                            'text-decoration': 'none',
                            'display': 'inline-block',
                            'font-size': '16px',
                            'margin': '4px 6px',
                            'margin-bottom': '20px',
                            'cursor': 'pointer'
                        }
                        )
        ]),
        style={
            'margin-left': '100px',
            'margin-top': '50px'
        },
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
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })

sample_call_data = html.Div([
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Call Dataset"),
            # html.Div(id='call-data')
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'left'
                    }
                    ),
        html.Button('CLOSED DATA', id='close',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'right'
                    })
    ],
        style={
            'padding-left': '30px'
        }),
    html.Div(id='show_data',
             style={
                 'padding-left': '20px',
                 'margin-top': '30px'
             })
],
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })
# over call dataset
call_data_list = []


@app.callback(dash.dependencies.Output('call-data', 'children'),
              [dash.dependencies.Input('upload-data_call', 'filename'),
               dash.dependencies.Input('upload-data_call', 'contents')
               ])
def add_call_dataset(filename, contents):
    if contents:
        contents = contents[0]
        filename = filename[0]
        call_data_list.append([filename, contents])
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
        contents = call_data_list[0][1]
        filename = call_data_list[0][0]
        df = parse_data(contents, filename)
        table = html.Div([
            html.H2(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
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
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Cell Dataset"),
            html.Div(id='cell-data')
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.Div([
            html.H3('ADD  CELL  DATASET',
                    style={
                        'background': 'gray',
                        'padding-top': '10px',
                        'padding-bottom': '10px',
                        'padding-left': '50px',
                        'color': 'white'
                    })
        ],
            style={
                'width': '700px',
                'margin-top': '50px',
                'padding-left': '30px'
            }),
    ]),
    dcc.Upload(
        id='upload-data_cell',
        children=html.Div([
            html.Button('ADD CELL DATA',
                        style={
                            'background-color': '#4CAF50',
                            'height': '50px',
                            'border': 'none',
                            'color': 'white',
                            'text-align': 'center',
                            'text-decoration': 'none',
                            'display': 'inline-block',
                            'font-size': '16px',
                            'margin': '4px 6px',
                            'margin-bottom': '20px',
                            'cursor': 'pointer'
                        }
                        )
        ]),
        style={
            'margin-left': '100px',
            'margin-top': '50px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
],
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })

sample_cell_data = html.Div([
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Cell Dataset"),
            # html.Div(id='cell-data')
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view_cell',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'left'
                    }
                    ),
        html.Button('CLOSED DATA', id='close_cell',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'right'
                    })
    ],
        style={
            'padding-left': '30px'
        }),
    html.Div(id='show_cell_data',
             style={
                 'padding-left': '20px',
                 'margin-top': '30px'
             })
],
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })

cell_data_list = []


@app.callback(dash.dependencies.Output('cell-data', 'children'),
              [dash.dependencies.Input('upload-data_cell', 'filename'),
               dash.dependencies.Input('upload-data_cell', 'contents')
               ])
def add_cell_dataset(filename, contents):
    if contents:
        contents = contents[0]
        filename = filename[0]
        cell_data_list.append([filename, contents])
        output_cell = []
        for x in cell_data_list:
            a = x[0].split('.')
            output_cell.append(dcc.Link(a[0], href='/Cell_Dataset/' + str(a[0])))
            output_cell.append(html.Br())
        name_cell = html.Div(
            children=output_cell
        )
        return name_cell


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
        contents = cell_data_list[0][1]
        filename = cell_data_list[0][0]
        df = parse_data(contents, filename)
        table = html.Div([
            html.H2(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
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
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Message Dataset"),
            html.Div(id='message-data')
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.Div([
            html.H3('ADD  MESSAGE  DATASET',
                    style={
                        'background': 'gray',
                        'padding-top': '10px',
                        'padding-bottom': '10px',
                        'padding-left': '50px',
                        'color': 'white'
                    })
        ],
            style={
                'width': '700px',
                'margin-top': '50px',
                'padding-left': '30px'
                # 'position':'fixed'
            }),
    ]),
    dcc.Upload(
        id='upload-data_message',
        children=html.Div([
            html.Button('ADD MESSAGE DATA',
                        style={
                            'background-color': '#4CAF50',
                            'height': '50px',
                            'border': 'none',
                            'color': 'white',
                            'text-align': 'center',
                            'text-decoration': 'none',
                            'display': 'inline-block',
                            'font-size': '16px',
                            'margin': '4px 6px',
                            'margin-bottom': '20px',
                            'cursor': 'pointer'
                        }
                        )
        ]),
        style={
            'margin-left': '100px',
            'margin-top': '50px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
],
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })

sample_message_data = html.Div([
    html.H1(
        children='CELLYZER',
        style={
            'textAlign': 'center',
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px'
        }),
    html.Div([
        html.H2(
            children='Dashboard',
            style={
                'color': 'white',
                'padding-left': '20px'
            }
        ),
        html.Div([
            html.H5("Message Dataset")
        ],
            style={
                'padding': '6px 8px 6px 20px',
                'text-decration': 'none',
                'font-size': '22px',
                'color': 'white',
                'display': 'block'
            }
        )
    ],
        style={
            'height': '100%',
            'width': '240px',
            'position': 'fixed',
            'z-index': '1',
            'top': '0',
            'left': '0',
            'background-color': '#111',
            'overflow-x': 'hidden',
            'padding-top': '20px',
            'margin-top': '8px'
        }
    ),
    html.Div([
        html.H4(id="file_name")
    ]),
    html.Div([
        html.Button('VIEW DATA', id='view_message',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'left'
                    }
                    ),
        html.Button('CLOSED DATA', id='close_message',
                    style={
                        'background-color': '#4CAF50',
                        'height': '50px',
                        'border': 'none',
                        'color': 'white',
                        'text-align': 'center',
                        'text-decoration': 'none',
                        'display': 'inline-block',
                        'font-size': '16px',
                        'margin': '4px 6px',
                        'margin-bottom': '20px',
                        'cursor': 'pointer',
                        'float': 'right'
                    })
    ],
        style={
            'padding-left': '30px'
        }),
    html.Div(id='show_message_data',
             style={
                 'padding-left': '20px',
                 'margin-top': '30px'
             })
],
    style={
        'margin-left': '222px',
        'padding': '0px 10px'
    })

message_data_list = []


@app.callback(dash.dependencies.Output('message-data', 'children'),
              [dash.dependencies.Input('upload-data_message', 'filename'),
               dash.dependencies.Input('upload-data_message', 'contents')
               ])
def add_message_dataset(filename, contents):
    if contents:
        contents = contents[0]
        filename = filename[0]
        message_data_list.append([filename, contents])
        output_message = []
        for x in message_data_list:
            a = x[0].split('.')
            output_message.append(dcc.Link(a[0], href='/Message_Dataset/' + str(a[0])))
            output_message.append(html.Br())
        name_message = html.Div(
            children=output_message
        )
        return name_message


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
        contents = message_data_list[0][1]
        filename = message_data_list[0][0]
        df = parse_data(contents, filename)
        table = html.Div([
            html.H2(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i, 'id': i} for i in df.columns]
            ),
            html.Hr(),
            html.Div('Raw Content'),
            html.Pre(contents[0:200] + '...', style={
                'whiteSpace': 'pre-wrap',
                'wordBreak': 'break-all'
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

# @app.callback(Output('Mygraph', 'figure'),
#             [
#                 Input('upload-data', 'contents'),
#                 Input('upload-data', 'filename')
#             ])
# def update_graph(contents, filename):
#     fig = {
#         'layout': go.Layout(
#             plot_bgcolor=colors["graphBackground"],
#             paper_bgcolor=colors["graphBackground"])
#     }

#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_data(contents, filename)
#         df = df.set_index(df.columns[0])
#         fig['data'] = df.iplot(asFigure=True, kind='scatter', mode='lines+markers', size=1)

#     return fig

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
