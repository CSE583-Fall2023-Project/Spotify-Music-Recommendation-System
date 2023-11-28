# home.py

import dash
from dash import dcc, html

dash.register_page(__name__, path = "/")

layout = html.Div([
    # Landing Page
    html.Div([
        # Headline
        html.H1("Spotify Music Exploration + Recommendation System", 
                className = "landing-headline"),

        # Button
        html.A("Start Your Journey", 
               href = "/explore", 
               className = "start-button"),
    ], className = "landing-page"),
])