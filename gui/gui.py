import base64
import datetime
import io
import plotly.graph_objs as go
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import folium

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

colors = {
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}
image_filename = 'cdr.jpg'
encoded_mage = base64.b64encode(open(image_filename, 'rb').read())
app.layout = html.Div([
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
        html.Img(
            src='data:image/jpg;base64,{}'.format(encoded_mage.decode()), 
            style={
            'width': '1300px',
            'height': '500px'
        } ),
        html.Div([
            html.H1("WELCOME"),
            html.H1('CDR DATA ANALYSIS')
        ],
            style={
                'position': 'absolute',
                'bottom': '200px',
                'background':'rgb(0,0,0)',
                'background':'rgb(0,0,0, 0.5)',
                'color': 'orange',
                'width': '1300px',
                'textAlign': 'center',
                'font-weight': '900',
                'font-size': '20px'
        } )
    ],
        style={
            'position':'relative',
            'max-width': '1300px',
            'margin': '0 auto'
        }),
        
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            html.Button('ADD CDR DATA File',
            style={
                'background-color': '#4CAF50',
                'height': '70px',
                'border': 'none',
                'color': 'white',
                'padding': '15px 32px',
                'text-align': 'center',
                'text-decoration': 'none',
                'display': 'inline-block',
                'font-size': '16px',
                'margin':'4px 6px',
                'margin-bottom': '20px',
                'cursor': 'pointer'
            }
            )
        ]),
        style={
            'margin-left': '100px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
    html.Div(id='output-data-upload'),
    html.Div([
        html.H3(
        children='Map Visualization',
        style={
            'color': 'orange',
            'background': 'black',
            'padding-top': '20px',
            'padding-bottom': '20px',
            'width': '350px',
            'padding-left': '90px'
        }),
        html.Div([
            html.H6('Longitude:'),
            dcc.Input(id="long", type='text', placeholder='Longitude')
            
        ]),
        html.Div([
            html.H6('Latitude:'),
            dcc.Input(id="lat", type='text', step='any', placeholder='Latitude')
            
        ]),
        html.Div([
            html.Button(id='submit_but', type='submit', children='Submit',
            style={
                'background-color': '#4CAF50',
                'color': 'white',
                'border': 'none',
                'font-size': '15px',

            })
        ],
        style={
            'margin-top': '20px',
            'margin-bottom': '20px',
            'padding-left': '20px'
        }) ,
        html.Iframe(id='map_new',
        style={
            'width': '100%',
            'height': '500px'
        }
    )
    ])

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
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df

@app.callback(Output('output-data-upload', 'children'),
            [
                Input('upload-data', 'contents'),
                Input('upload-data', 'filename')
            ])
def update_table(contents, filename):
    table = html.Div()

    if contents:
        contents = contents[0]
        filename = filename[0]
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

@app.callback(Output('map_new', 'srcDoc'),
            [
                Input('long', 'value'),
                Input('lat', 'value'),
                Input('submit_but', 'n_clicks')
            ])
def show_map(longitude, latitude, clicks):
    try:
        if clicks is not None:
            mapit = folium.Map(location=[float(longitude), float(latitude)], zoom_start=12)
            folium.Marker([longitude, latitude], popup='<strong>Location One</strong>').add_to(mapit)
            mapit.save( 'map.html')
        
            return open('map.html', 'r').read()
    except ValueError:
        print("Not a float")

if __name__ == '__main__':
    app.run_server(debug=True)