"""
Defines utility functions and Dash callbacks for "Recommended Songs" section in Recom page.

This module contains utility and callback functions for retrieving and updating
recommended user playlist based on user_id.
"""


# Import packages
import dash
from dash import Output, Input, State, html
from dash.exceptions import PreventUpdate
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from utils.database import UserRecommendation, SpotifyData, engine
from utils.pages.login.usermatch import check_user

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)


# Function for recommended playlist retrieval
def fetch_user_playlist(user_id, session=None):
    """
    Retrieves user playlist data for given user from UserRecommendation and SpotifyData.

    Arguments:
        user_id (str): User ID.
        session: SQLAlchemy session (optional).

    Returns three lists containing song names, artist names, and song URLs.
    """
    own_session = False
    if session is None:
        session = Session()
        own_session = True
    else:
        session = session

    try:
        login_user_playlist = session.query(UserRecommendation).\
            filter_by(user_id=user_id).all()
        print(f"Fetched recommendations: {login_user_playlist}")
        songs_list, artists_list, urls_list = [], [], []
        for recommendation in login_user_playlist:
            song = session.query(SpotifyData).\
                filter_by(song_id=recommendation.song_id).first()
            if song:
                songs_list.append(song.song_name)
                artists_list.append(song.artist_name)
                urls_list.append(song.song_id)
        return songs_list, artists_list, urls_list

    except SQLAlchemyError as excep:
        print(f"Error accessing database: {excep}")
        return [], [], []
    finally:
        if own_session:
            session.close()


# Callbacks for playlist data storage
@dash.callback(
    [Output("playlist-song-store", "data"),
     Output("playlist-artist-store", "data"),
     Output("playlist-url-store", "data")],
    Input("login-button", "n_clicks"),
    [State("first-name", "value"),
     State("last-name", "value")]
)
def get_recommendations(n_clicks, first_name, last_name):
    """
    Retrieves recommended playlist data to playlist stores upon successful login.

    Arguments:
        n_clicks (int): Number of clicks on the login button.
        first_name (str): User's first name.
        last_name (str): User's last name.
    
    Returns a tuple containing lists of songs, artists, and URLs.
    """
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            uid = user_data["user_id"]
            return fetch_user_playlist(uid)
    raise PreventUpdate


# Callbacks for updating recommended playlists
@dash.callback(
    Output("user-playlist-container", "children"),
    [Input("playlist-song-store", "data"),
     Input("playlist-artist-store", "data"),
     Input("playlist-url-store", "data")]
)
def update_user_playlist(songs_list, artists_list, urls_list):
    """
    Updates the user playlist container with recommended songs.

    Arguments:
        songs_list (list): List of song names.
        artists_list (list): List of artist names.
        urls_list (list): List of song URLs.
    
    Returns a Dash HTML Ordered List component to display recommended playlist.
    """
    if songs_list and artists_list and urls_list:
        list_items = []
        base_url = "https://open.spotify.com/track/"
        for song, artist, url in zip(songs_list, artists_list, urls_list):
            track_url = base_url + url
            play_button = html.Img(
                src="../../../assets/icon/spotify-play-button.png",
                className="play-button"
            )
            song_link = html.A(
                [play_button, song],
                href=track_url,
                target="_blank",
                className="song-name"
            )
            item = html.Li([
                song_link,
                html.Div(artist, className="song-artist")
            ])
            list_items.append(item)
        return html.Ol(list_items)
    raise PreventUpdate
