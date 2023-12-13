"""
Recommendation page for the Spotify Music Exploration/Recommendation System. 

For logged-in users, this pages displays their profile information, a radar chart 
visualizing their musical preferences, and a playlist suggesting 10 new tracks.  
It offers a personalized experience catering to users' music tastes.
"""

# Import packages
from dash import dcc, register_page, html

from utils.pages.recom.callbacks import *
from utils.page_template import portfolio_wrapper

# Register the page
register_page(
    __name__,
    path="/reco",
    title="Your Playlist - Spotify Music Recommendation System"
)

# User Profile
user_info_display = \
    html.Div([
        html.Div(id="user-profile-container"),
        html.Hr(className="profile-divider"),
    ], className="user-profile-container")

# User Music Profile
user_music_profile = \
    html.Div([
        # Music Style
        html.Div([
            html.Span("Your Music Taste", className="music-style-title"),
            html.Div([
                dcc.Graph(figure={}, id="user-attribute-radar-chart")
            ], className="user-attribute-radar-chart")
        ], className="music-style-container"),

        # Recommended Songs
        html.Div([
            html.Span("Recommended Songs", className="recommended-songs-title"),
            html.Div(
                id="user-playlist-container",
                className="user-playlist-container"
            ),
        ], className="recommended-songs-container")
    ], className="user-music-profile-container")

# Logout Button
logout_button = html.Div([
    dcc.Link(
        html.Button(
            "Logout",
            id="logout-button",
            className="logout-button"
        ), href="/"
    )
], className="logout-button-container")

# Page Layout
layout = \
    portfolio_wrapper(
        user_info_display,
        user_music_profile,
        logout_button
    )
