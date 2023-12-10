# explore.py

"""
Explore page for Spotify Music Exploration/Recommendation System.

This page displays interactive visualizations on historical music insights.
Visualization #1: Line chart illustrating trend of musical attributes over time.
Visualization #2: Radar chart depicting musical attributes of selected song.
"""

# Import packages
from dash import dcc, html, register_page

from utils.pages.explore.callbacks import *
from utils.page_template import portfolio_wrapper

# Register the page
register_page(__name__, path="/explore",
              title="Explore Music - Spotify Music Recommendation System")

# Visualization #1: Trend of Musical Attributes Over Time
Music_Trend = \
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
            html.A("⌵", href="#02-song-attribute", className="scroll-arrow")
        )
    ], className="content-panel"
             )

# Visualization #2: Radar Chart for Selected Song
Music_Attribute = \
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
                className="song-selecting-dropdown"
            )
        ], className="drop-down-container"),

        # Radar Chart
        html.Div([
            dcc.Graph(figure={}, id="song-attribute-radar-chart")
        ], className="song-attribute-radar-chart")
    ], className="content-panel"
             )

# Page Layout
layout = \
    portfolio_wrapper(
        Music_Trend,
        Music_Attribute
    )
