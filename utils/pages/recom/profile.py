import pandas as pd
import plotly.express as px
from dash import callback, Output, Input
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import sessionmaker
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

from utils.database import SpotifyData, UserSongs, DataByYear, engine
from utils.pages.explore.visuals import empty_radar_plot

# Set up the SQLAlchemy session
Session = sessionmaker(bind=engine)

# Define global variables
attributes = ["acousticness", "danceability", "energy", "instrumentalness",
              "liveness", "speechiness", "valence"]


# Visualization
@callback(
    Output("user-attribute-radar-chart", "figure"),
    Input("song-selecting-dropdown", "value")
)
def update_song_attributes(user_id, session=None):
    if session is not None:
        session = session
    else:
        session = Session()
    if user_id:
        user_music_profile_query = session.query(
            UserSongs.song_id, 
            UserSongs.listening_count,
            SpotifyData.song_name,
            SpotifyData.artist_name,
            SpotifyData.year,
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
            UserSongs.user_id == user_id),
        user_music_profile_df = pd.read_sql(user_music_profile_query.statement, user_music_profile_query.session.bind)
        if not user_music_profile_df.empty:
            user_music_profile = user_music_profile_df.iloc[0]
            radar_data = pd.DataFrame({"Attribute": attributes,
                                       "Value": [user_music_profile[attr] for attr in attributes]})
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

