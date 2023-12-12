import pandas as pd
import numpy as np
import plotly.express as px
from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from utils.database import UserSongs, SpotifyData, engine
from utils.pages.login.usermatch import check_user
from utils.pages.explore.visuals import empty_radar_plot

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)

# Define function to fetch user's song data
def fetch_user_song_data(user_id, session=None):
    own_session = False
    if session is None:
        session = Session()
        own_session = True

    try:
        print("Received user ID:", user_id)
        # Query to fetch user's song data
        user_song_data_query = session.query(
            UserSongs.song_id, 
            UserSongs.listening_count,
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
        )
        print(f"Fetched songs: {user_song_data_query}")
        user_song_data = pd.read_sql(user_song_data_query.statement, user_song_data_query.session.bind)
        return user_song_data

    except SQLAlchemyError as e:
        print(f"Error accessing database: {e}")
        return pd.DataFrame()
    finally:
        if own_session:
            session.close()


# Define callback for updating the radar plot
@callback(
    Output("user-attribute-radar-chart", "figure"),
    Input("login-button", "n_clicks"),
    [State("first-name", "value"), State("last-name", "value")]
)
def update_song_attributes(n_clicks, first_name, last_name):
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            user_id = user_data["user_id"]
            print("Received user ID:", user_id)
            user_song_data = fetch_user_song_data(user_id)
            print("Fetching User Data...")

            if not user_song_data.empty:
                attributes = ["acousticness", "danceability", "energy", "instrumentalness", "liveness", "speechiness", "valence"]
                weights = user_song_data["listening_count"].values

                weighted_averages = {}
                for attribute in attributes:
                    values = user_song_data[attribute].values
                    weighted_average = np.sum(values * weights) / np.sum(weights)
                    weighted_averages[attribute] = weighted_average

                radar_data = pd.DataFrame({
                    "Attribute": attributes,
                    "Value": [weighted_averages[attr] for attr in attributes]
                })

                fig = px.line_polar(radar_data,
                                r="Value",
                                theta="Attribute",
                                line_close=True)
                fig.update_traces(fill="toself",
                                fillcolor="rgba(29, 185, 84, 0.5)",
                                line=dict(color="#1db954"))
                fig.update_layout(plot_bgcolor="#121212",
                                paper_bgcolor="#121212",
                                font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14))
                return fig

            return empty_radar_plot()

        return empty_radar_plot()

    raise PreventUpdate
