"""
app.py
Author: Nathan Wilson
Contact: nathan.wilson3@outlook.com
Date: 2024-07-27
Version: 1.3
Purpose: This is the main application file for the CS-340 Dashboard. It provides a web interface for interacting with the AnimalShelter database.
Issues: None known
"""

import os
from dotenv import load_dotenv
import logging
import dash
import dash_leaflet as dl
from dash import dcc, html, dash_table
import plotly.express as px
from dash.dependencies import Input, Output, State
import base64
import pandas as pd
from animalShelter import AnimalShelter

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()
MONGO_CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_CONNECTION_STRING or not DB_NAME:
    logging.error("Environment variables for MongoDB connection are not set correctly.")
    exit(1)

# Connect to the AnimalShelter database and collection
try:
    shelter = AnimalShelter(MONGO_CONNECTION_STRING, DB_NAME, "AnimalShelter")
    logging.info("Successfully connected to the database and accessed the collection.")
except Exception as e:
    logging.error(f"Failed to connect to the database: {e}")
    exit(1)

# Fetch data from the database
try:
    data = shelter.read({})
    df = pd.DataFrame(data)
    if not df.empty:
        df.drop(columns=['_id'], inplace=True)
    logging.info("Successfully fetched data from the database.")
except Exception as e:
    logging.error(f"Failed to fetch data: {e}")
    df = pd.DataFrame()  # Use an empty DataFrame to avoid crashing

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and encode the image
image_filename = 'my-image.png'  # replace with your own image
try:
    encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode()
    logging.info("Successfully loaded and encoded the image.")
except Exception as e:
    logging.error(f"Failed to load and encode the image: {e}")
    encoded_image = ""

# Helper function to construct query based on rescue type
def construct_query(rescue_type):
    if rescue_type == 'Water Rescue':
        return {'breed': {'$in': ['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland']}}
    elif rescue_type == 'Mountain or Wilderness Rescue':
        return {'breed': {'$in': ['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler']}}
    elif rescue_type == 'Disaster or Individual Tracking':
        return {'breed': {'$in': ['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler']}}
    else:
        return {}

# Define the layout of the app
app.layout = html.Div([
    html.Center(html.B(html.H1('Austin Animal Shelter Dashboard'))),
    html.Hr(),
    html.Div([
        html.Img(
            src=f'data:image/png;base64,{encoded_image}',
            style={
                'width': '25%',  # Adjust the width as needed
                'height': 'auto',
                'display': 'block',
                'margin-left': 'auto',
                'margin-right': 'auto',
                'margin-top': '10px'  # Adjust this value to move the image down from the top
            }
        ),
        dcc.RadioItems(
            id='filter-type',
            options=[
                {'label': 'All', 'value': 'all'},
                {'label': 'Cats', 'value': 'Cat'},
                {'label': 'Dogs', 'value': 'Dog'}
            ],
            value='all',
            labelStyle={'display': 'inline-block'},
            style={'text-align': 'center', 'margin-top': '20px'}
        ),
        # Add rescue type filter
        dcc.RadioItems(
            id='rescue-type-radio',
            options=[
                {'label': 'Water Rescue', 'value': 'Water Rescue'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain or Wilderness Rescue'},
                {'label': 'Disaster or Individual Tracking', 'value': 'Disaster or Individual Tracking'},
                {'label': 'All', 'value': 'All'}
            ],
            value='All',
            labelStyle={'display': 'inline-block'},
            style={'text-align': 'center', 'margin-top': '20px'}
        ),
    ]),
    # Input fields for CRUD operations
    html.Hr(),
    html.Div([
        dcc.Input(id='animal_id', type='text', placeholder='Animal ID'),
        dcc.Input(id='name', type='text', placeholder='Name'),
        dcc.Input(id='animal_type', type='text', placeholder='Type'),
        dcc.Input(id='breed', type='text', placeholder='Breed'),
        dcc.Input(id='color', type='text', placeholder='Color'),
        dcc.Input(id='age', type='number', placeholder='Age'),
        dcc.Input(id='adopted', type='text', placeholder='Adopted (True/False)'),
        html.Button('Create', id='create-button', n_clicks=0),
        html.Button('Update', id='update-button', n_clicks=0),
        html.Button('Delete', id='delete-button', n_clicks=0),
    ], style={'display': 'flex', 'justify-content': 'center'}),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[{"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns],
        data=df.to_dict('records'),
        editable=True,
        filter_action="native",
        sort_action="native",
        sort_mode="multi",
        row_selectable="multi",
        row_deletable=False,
        selected_rows=[],
        page_action="native",
        page_current=0,
        page_size=10,
    ),
    html.Br(),
    html.Hr(),
    html.Div(className='row', style={'display': 'flex'}, children=[
        html.Div(id='graph-id', className='col s12 m6'),
        html.Div(id='map-id', className='col s12 m6')
    ])
])

# Handle CRUD operations and filter update in a single callback
@app.callback(
    Output('datatable-id', 'data'),
    [Input('create-button', 'n_clicks'),
     Input('update-button', 'n_clicks'),
     Input('delete-button', 'n_clicks'),
     Input('filter-type', 'value'),
     Input('rescue-type-radio', 'value')],
    [State('animal_id', 'value'),
     State('name', 'value'),
     State('animal_type', 'value'),
     State('breed', 'value'),
     State('color', 'value'),
     State('age', 'value'),
     State('adopted', 'value'),
     State('datatable-id', 'derived_virtual_selected_rows')]
)
def handle_operations_and_update_data(n_create, n_update, n_delete, filter_type, rescue_type, animal_id, name, animal_type, breed, color, age, adopted, selected_rows):
    ctx = dash.callback_context
    if not ctx.triggered:
        return dash.no_update

    button_id = ctx.triggered[0]['prop_id'].split('.')[0]
    
    if button_id == 'create-button' and n_create > 0:
        new_animal = {
            "animal_id": animal_id,
            "name": name,
            "animal_type": animal_type,
            "breed": breed,
            "color": color,
            "age": age,
            "adopted": adopted.lower() == 'true'
        }
        shelter.create(new_animal)
    
    elif button_id == 'update-button' and n_update > 0:
        if selected_rows:
            selected_row = selected_rows[0]
            update_data = {
                "name": name,
                "animal_type": animal_type,
                "breed": breed,
                "color": color,
                "age": age,
                "adopted": adopted.lower() == 'true'
            }
            query = {"animal_id": animal_id}
            shelter.update(query, update_data)
    
    elif button_id == 'delete-button' and n_delete > 0:
        if selected_rows:
            selected_row = selected_rows[0]
            query = {"animal_id": animal_id}
            shelter.delete(query)
    
    query = construct_query(rescue_type)
    if filter_type != 'all':
        query["animal_type"] = filter_type
    
    data = shelter.read(query)
    return pd.DataFrame(data).drop(columns=['_id']).to_dict('records')

# Update bar graph based on data table
@app.callback(
    Output('graph-id', "children"),
    [Input('datatable-id', "derived_virtual_data")]
)
def update_graphs(viewData):
    try:
        dff = pd.DataFrame.from_dict(viewData)
        if dff.empty:
            return dash.no_update
        fig = px.bar(dff, x='breed', title='Breed Distribution', labels={'x': 'Breed', 'y': 'Count'})
        fig.update_layout(xaxis_title='Breed', yaxis_title='Count')
        return [dcc.Graph(figure=fig)]
    except Exception as e:
        logging.error(f"Failed to update graphs: {e}")
        return []

# Update map based on selected data entry
@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_virtual_data"),
     Input('datatable-id', "derived_virtual_selected_rows")]
)
def update_map(viewData, selected_rows):
    if viewData is None or selected_rows is None or len(selected_rows) == 0:
        return dash.no_update
    
    dff = pd.DataFrame.from_dict(viewData)
    
    # Plot multiple markers if multiple rows are selected
    markers = []
    lats = []
    lons = []
    for row in selected_rows:
        if 'location_lat' in dff.columns and 'location_long' in dff.columns:
            lat = dff.iloc[row]['location_lat']
            lon = dff.iloc[row]['location_long']
            lats.append(lat)
            lons.append(lon)
            marker = dl.Marker(position=[lat, lon], children=[
                dl.Tooltip(dff.iloc[row]['breed']),
                dl.Popup([html.H1("Animal Name"), html.P(dff.iloc[row]['name'])])
            ])
            markers.append(marker)
    
    if not markers:
        return ["No valid coordinates available"]

    # Calculate the bounds to fit all markers
    min_lat = min(lats)
    max_lat = max(lats)
    min_lon = min(lons)
    max_lon = max(lons)
    bounds = [[min_lat, min_lon], [max_lat, max_lon]]

    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, bounds=bounds, children=[
            dl.TileLayer(id="base-layer-id"),
            *markers  # Unpack all markers into the map
        ])
    ]

if __name__ == '__main__':
    app.run_server(debug=True)
