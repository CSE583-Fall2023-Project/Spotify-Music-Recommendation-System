# explore.py
"""
To launch the app, type command "python app.py" in terminal
Then navigate to the http link
"""

# Import packages
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, callback, Output, Input

# Register the page
dash.register_page(__name__, path = "/explore")


# Load data
data_by_year = pd.read_csv("../data/data_by_year.csv")
spotify_data = pd.read_csv("../data/spotify_data.csv")

# Determine the range and marks for the slider 
min_year = data_by_year["year"].min()
max_year = data_by_year["year"].max()

# Create decades list
decades = list(range(min_year + (10 - min_year % 10), max_year + 1, 10))
decades = [min_year] + decades if min_year not in decades else decades
decades += [max_year] if max_year not in decades else []

# Create marks
marks = {int(year): {"label": str(year)} for year in decades}

# Songs and attributes
attributes = ["acousticness", "danceability", "energy", "instrumentalness", 
              "liveness", "speechiness", "valence"]
sorted_songs = spotify_data.sort_values(by = "popularity", ascending = False)\
              ["song_name"].unique()


# Define the app layout and components
layout = html.Div([
    
    # Visualization #1: Trend of Musical Attributes Over Time
    html.Div(id = "01-music-trend", children = [
        # Section Title
        html.H2("How Did Music Evolve Over Time?", 
                className = "section-title"),
        html.H3("Trend of Musical Attributes Over Years", 
                className = "section-subtitle"), 
        html.Hr(className = "section-divider"),
        
        # Checklist
        html.Div([
            dcc.Checklist(
                id = "attribute-checklist",
                options = attributes,
                value = ["acousticness"],
                className = "attribute-checklist"
            )
        ], className = "checklist-container"), 
        
        # Line Chart 
        html.Div([
            dcc.Graph(figure = {}, id = "attribute-trend-line-chart")
        ], className = "graph-container"), 
        
        # Range Slider
        dcc.RangeSlider(
            id = "year-range-slider",
            min = min_year,
            max = max_year,
            value = [min_year, max_year],
            marks = marks,
            step = 1, 
            className = "year-range-slider"
        ),
    
        # Navigating Arrow
        html.Div(
            html.A("⌵", href = "#02-song-attribute", className = "scroll-arrow"),
            style = {"textAlign": "center", "fontSize": "36px", "padding": "20px", "color": "#a7a7a7"}
        )
    ], className = "content-panel"),
    
    
    # Visualization #2: Radar Chart for Selected Song
    html.Div(id = "02-song-attribute", children = [
        # Section Title
        html.H2("What Are the Characters of Individual Songs?", 
                className = "section-title"),
        html.H3("Musical attributes for Selected Song", 
                className = "section-subtitle"), 
        html.Hr(className = "section-divider"),
        
        # Searchable Dropdown
        html.Div([
            dcc.Dropdown(
                id = "song-selecting-dropdown",
                options = [{"label": song, "value": song} for song in sorted_songs],
                placeholder = "Select a song",
                searchable = True,
                style = {"width": "50%", "margin": "20px auto"}
            )
        ]),

        # Radar Chart
        html.Div([
            dcc.Graph(figure = {}, id = "song-attribute-radar-chart")
        ])
    ], className = "content-panel")
    
])


# Add controls to build the interaction
# Visualization #1
@callback(
    Output(component_id = "attribute-trend-line-chart", component_property = "figure"),
    Input(component_id = "attribute-checklist", component_property = "value"),
    Input(component_id = "year-range-slider", component_property = "value")
)

def update_attribute_trend(selected_attributes, selected_years):
    filtered_data = data_by_year[(data_by_year["year"] >= selected_years[0]) & 
                                 (data_by_year["year"] <= selected_years[1])]
    fig = px.line(filtered_data, x = "year", y = selected_attributes)
    
    # Update plot layout
    fig.update_layout(
        plot_bgcolor = "#121212",
        paper_bgcolor = "#121212",
        font = dict(family = "Gill Sans, Arial, sans-serif", 
                    color = "#f2f2f2")
    )
    return fig


# Visualization #2
@callback(
    Output("song-attribute-radar-chart", "figure"), 
    Input("song-selecting-dropdown", "value")
)

def update_song_attributes(selected_song):
    if selected_song:
        song_data = spotify_data[spotify_data["song_name"] == selected_song].iloc[0]
        radar_data = pd.DataFrame({
            "Attribute": attributes,
            "Value": [song_data[attr] for attr in attributes]
        })
        fig = px.line_polar(
            radar_data, 
            r = "Value", 
            theta = "Attribute", 
            line_close = True)
        fig.update_traces(
            fill = "toself", 
            fillcolor = "rgba(29, 185, 84, 0.5)", 
            line = dict(color = "#1db954")
        )
        fig.update_layout(
            plot_bgcolor = "#121212", 
            paper_bgcolor = "#121212",
            font = dict(family = "Gill Sans, Arial, sans-serif", color = "#1db954", size = 14)
        )
        return fig
    else:
        fig = px.line_polar()
        fig.update_layout(
            plot_bgcolor = "#121212", 
            paper_bgcolor = "#121212",
            font = dict(family = "Gill Sans, Arial, sans-serif", color = "#1db954", size = 14)
        )
        return fig   
