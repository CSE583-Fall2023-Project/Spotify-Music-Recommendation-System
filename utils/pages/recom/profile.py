"""
Defines utility functions and Dash callbacks for "Your Music Taste" section in Recom page.

This module contains utility and callback functions for retrieving attributes of
user's listening history and updating user's music preferences on a radar chart.
"""

# Import packages
import pandas as pd
import numpy as np
import plotly.express as px
from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate
from sqlalchemy import func, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from utils.database import UserSongs, SpotifyData, engine
from utils.pages.login.usermatch import check_user
from utils.pages.explore.visuals import empty_radar_plot

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)


# Function for listening history retrieval
def fetch_user_song_data(user_id, session=None):
    """
    Retrieves the top 10 most listened song and their attributes for given user
    from SpotifyData and UserSongs.

    Arguments:
        user_id (str): User ID.
        session: SQLAlchemy session (optional).

    Returns a pandas DataFrame containing user's listening history and song
    attributes.
    """
    own_session = False
    if session is None:
        session = Session()
        own_session = True

    try:
        print("Fetching Listening History for User", user_id)

        # Check if the user has any records in UserSongs
        user_songs_exist = session.query(UserSongs).filter_by(user_id=user_id).first()
        if not user_songs_exist:
            print(f"No records found for user ID: {user_id}")
            return pd.DataFrame()

        # Query to fetch user's top 10 most listened songs and their details
        user_song_data_query = session.query(
            UserSongs.song_id,
            func.sum(UserSongs.listening_count).label("total_listening_count"),
            SpotifyData.valence,
            SpotifyData.acousticness,
            SpotifyData.danceability,
            SpotifyData.energy,
            SpotifyData.instrumentalness,
            SpotifyData.liveness,
            SpotifyData.speechiness
        ).join(
            SpotifyData, UserSongs.song_id == SpotifyData.song_id
        ).filter(
            UserSongs.user_id == user_id
        ).group_by(
            UserSongs.song_id
        ).order_by(
            desc("total_listening_count")
        ).limit(10)

        user_song_data = pd.read_sql(user_song_data_query.statement, session.bind)
        return user_song_data

    except SQLAlchemyError as excep:
        print(f"Error accessing database: {excep}")
        return pd.DataFrame()
    finally:
        if own_session:
            session.close()


# Callbacks for user song storage
@callback(
    [Output("user-song-store", "data")],
    Input("login-button", "n_clicks"),
    [State("first-name", "value"),
     State("last-name", "value")]
)
def get_user_songs(n_clicks, first_name, last_name):
    """
    Retrieves user song data to user-song-store upon successful login.

    Arguments:
        n_clicks (int): Number of clicks on the login button.
        first_name (str): User's first name.
        last_name (str): User's last name.
    
    Returns a list containing user song data to a dcc store.
    """
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            uid = user_data["user_id"]
            print(f"====== WELCOME USER {uid} ======")
            user_song_data = fetch_user_song_data(uid).to_dict("records")
            return [user_song_data]
    raise PreventUpdate


# Callbacks for updating user music taste radar plot
@callback(
    Output("user-attribute-radar-chart", "figure"),
    Input("user-song-store", "data")
)
def update_user_song_attributes(user_song_data):
    """
    Updates radar chart with user song attributes.

    Arguments:
        user_song_data (list): A list of user song data from user-song-store.
    
    Returns a plotly figure with radar chart displaying weighted average of
    user listening history attributes.
    """
    print("Plotting User Music Taste...")

    if user_song_data:
        user_song_df = pd.DataFrame(user_song_data)
        attributes = ["acousticness", "danceability", "energy",
                      "instrumentalness", "liveness", "speechiness", "valence"]
        weights = user_song_df["total_listening_count"].values
        attribute_values = user_song_df[attributes].values
        weighted_averages = \
            np.sum(attribute_values * weights[:, np.newaxis], axis=0) / np.sum(weights)

        radar_data = pd.DataFrame({
            "Attribute": attributes,
            "Value": weighted_averages
        })

        fig = px.line_polar(
            radar_data,
            r="Value",
            theta="Attribute",
            line_close=True
        )
        fig.update_traces(
            fill="toself",
            fillcolor="rgba(29, 185, 84, 0.5)",
            line={"color": "#1db954"}
        )
        fig.update_layout(
            plot_bgcolor="rgba(0, 0, 0, 0)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font={"family": "Gill Sans, Arial, sans-serif", "color": "#1db954", "size": 14}
        )
        return fig

    print("Failed to Retrieve User Listening History")
    return empty_radar_plot()
