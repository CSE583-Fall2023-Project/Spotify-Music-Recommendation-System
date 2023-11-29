# explore.py
"""


"""

# Import packages
import plotly.express as px
import dash
from dash import dcc, html, register_page

from utils.pages.explore.callbacks import *
from utils.page_template import portfolio_wrapper

register_page(__name__, path="/explore", title="Explore")

# Visualization #1: Trend of Musical Attributes Over Time
Visualization_1 = \
    html.Div(id="01-music-trend", children=[
        # Section Title
        html.H2("How Did Music Evolve Over Time?",
                className="section-title"),
        html.H3("Trend of Musical Attributes Over Years",
                className="section-subtitle"),
        html.Hr(className="section-divider"),

        # Checklist
        html.Div([
            dcc.Checklist(
                id="attribute-checklist",
                options=attributes,
                value=["acousticness"],
                className="attribute-checklist"
            )
        ], className="checklist-container"),

        # Line Chart 
        html.Div([
            dcc.Graph(figure={}, id="attribute-trend-line-chart")
        ], className="graph-container"),

        # Range Slider
        dcc.RangeSlider(
            id="year-range-slider",
            min=min_year,
            max=max_year,
            value=[min_year, max_year],
            marks=marks,
            step=1,
            className="year-range-slider"
        ),

        # Navigating Arrow
        html.Div(
            html.A("⌵", href="#02-song-attribute", className="scroll-arrow"),
            style={"textAlign": "center", "fontSize": "36px", "padding": "20px", "color": "#a7a7a7"}
        )
    ], className="content-panel"
             )

# Visualization #2: Radar Chart for Selected Song
Visualization_2 = \
    html.Div(id="02-song-attribute", children=[
        # Section Title
        html.H2("What Are the Characters of Individual Songs?",
                className="section-title"),
        html.H3("Musical attributes for Selected Song",
                className="section-subtitle"),
        html.Hr(className="section-divider"),

        # Searchable Dropdown
        html.Div([
            dcc.Dropdown(
                id="song-selecting-dropdown",
                options=[{"label": song, "value": song} for song in sorted_songs],
                placeholder="Select a song",
                searchable=True,
                style={"width": "50%", "margin": "20px auto"}
            )
        ], className="song-selecting-dropdown"),

        # Radar Chart
        html.Div([
            dcc.Graph(figure={}, id="song-attribute-radar-chart")
        ], className="song-attribute-radar-chart")
    ], className="content-panel"
             )

layout = \
    portfolio_wrapper(
        Visualization_1,
        Visualization_2
    )
