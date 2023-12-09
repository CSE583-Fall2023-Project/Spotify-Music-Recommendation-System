from sqlalchemy.orm import sessionmaker
from dash.exceptions import PreventUpdate
from dash import Output, Input, State, html
import dash
import json

from utils.database import UserRecommendation, SpotifyData, engine
from utils.pages.login.usermatch import check_user

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)
session = Session()


@dash.callback(
    [Output('playlist-song-store', 'data'),
     Output('playlist-artist-store', 'data')],
    Input('login-button', 'n_clicks'),
    [State('first-name', 'value'),
     State('last-name', 'value')]
)
def get_recommendations(n_clicks, first_name, last_name):
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            uid = user_data['user_id']
            login_user_playlist = session.query(UserRecommendation).filter_by(user_id=uid).all()
            # Get song and artist names from ids
            songs_list, artists_list = [], []
            for recommendation in login_user_playlist:
                song = session.query(SpotifyData).filter_by(song_id=recommendation.song_id).first()
                if song:
                    songs_list.append(song.song_name)
                    artists_list.append(song.artist_name)
            session.close()
            return songs_list, artists_list

    raise PreventUpdate


@dash.callback(
    Output('user-playlist-container', 'children'),
    [Input('playlist-song-store', 'data'),
     Input('playlist-artist-store', 'data')]
)
def update_user_playlist(songs_list, artists_list):
    if songs_list and artists_list:
        list_items = []
        for song, artist in zip(songs_list, artists_list):
            item = html.Li([
                html.Div(song, className="song-name"),
                html.Div(artist, className="song-artist")
            ])
            list_items.append(item)
        return html.Ol(list_items)
    raise PreventUpdate

