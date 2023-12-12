import pandas as pd
import numpy as np
import plotly.express as px
from dash import callback, Output, Input, State
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
        user_song_data_df = pd.read_sql(user_song_data_query.statement, user_song_data_query.session.bind)
        return user_song_data_df

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
    [State('first-name', 'value'), State('last-name', 'value')]
)
def update_song_attributes(n_clicks, first_name, last_name):
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            user_id = user_data['user_id']
            print(user_id)
            user_song_data = fetch_user_song_data(user_id)

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

    raise PreventUpdate



# import pandas as pd
# import numpy as np
# import plotly.express as px
# from dash import callback, Output, Input
# from sqlalchemy.orm import sessionmaker

# from utils.database import SpotifyData, UserSongs, engine
# from utils.pages.explore.visuals import empty_radar_plot

# # Set up the SQLAlchemy session
# Session = sessionmaker(bind=engine)

# # Define global variables
# attributes = ["acousticness", "danceability", "energy", "instrumentalness",
#               "liveness", "speechiness", "valence"]

# # Visualization
# @callback(
#     Output("user-attribute-radar-chart", "figure"),
#     Input("user-id", "value")
# )
# def update_song_attributes(user_id, session=None):
#     if session is not None:
#         session = session
#     else:
#         session = Session()

#     if user_id:
#         user_music_profile_query = session.query(
#             UserSongs.song_id, 
#             UserSongs.listening_count,
#             SpotifyData.song_name,
#             SpotifyData.artist_name,
#             SpotifyData.year,
#             SpotifyData.valence,
#             SpotifyData.acousticness,
#             SpotifyData.danceability,
#             SpotifyData.energy,
#             SpotifyData.instrumentalness,
#             SpotifyData.liveness,
#             SpotifyData.speechiness
#         ).join(
#             SpotifyData, UserSongs.song_id == SpotifyData.song_id
#         ).filter(
#             UserSongs.user_id == user_id
#         )
#         user_music_profile_df = pd.read_sql(user_music_profile_query.statement, user_music_profile_query.session.bind)
        
#         if not user_music_profile_df.empty:
#             weights = user_music_profile_df["listening_count"].values
#             weighted_averages = {}
#             for attribute in attributes:
#                 values = user_music_profile_df[attribute].values
#                 weighted_average = np.sum(values * weights) / np.sum(weights)
#                 weighted_averages[attribute] = weighted_average

#             radar_data = pd.DataFrame({
#                 "Attribute": attributes,
#                 "Value": [weighted_averages[attr] for attr in attributes]
#             })

#             fig = px.line_polar(radar_data,
#                                 r="Value",
#                                 theta="Attribute",
#                                 line_close=True)
#             fig.update_traces(fill="toself",
#                               fillcolor="rgba(29, 185, 84, 0.5)",
#                               line=dict(color="#1db954"))
#             fig.update_layout(plot_bgcolor="#121212",
#                               paper_bgcolor="#121212",
#                               font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14))
#             return fig

#         return empty_radar_plot()

#     return empty_radar_plot()
