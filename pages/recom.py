# recom.py

"""
Recommendation page for the Spotify Music Exploration/Recommendation System. 

"""

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

# Recommended Songs
recommended_songs = \
    html.Div([
        html.Div([
            html.Div(html.H1("Your Music Taste",
                             className="music-style-title"))
        ], className="music-style-container"),
        html.Div([
            html.Span("Recommended Songs",
                      className="recommended-songs-title"),
            html.Div(id="user-playlist-container",
                     className="user-playlist-container"),
        ], className="recommended-songs-container")
    ], className="user-music-profile-container")

# Logout Button
logout_button = dcc.Link(
    html.Button("Logout",
                id="logout-button",
                className="logout-button"),
    href="/"
)

# Page Layout
layout = \
    portfolio_wrapper(
        user_info_display,
        recommended_songs,
        logout_button
    )
