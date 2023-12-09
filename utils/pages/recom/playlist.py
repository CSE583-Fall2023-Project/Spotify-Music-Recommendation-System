from sqlalchemy.orm import sessionmaker
from dash.exceptions import PreventUpdate
from dash import Output, Input, State, html
import dash

from utils.database import UserRecommendation, SpotifyData, engine
from utils.pages.login.usermatch import check_user

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)
session = Session()


@dash.callback(
    [Output('playlist-song-store', 'data'),
     Output('playlist-artist-store', 'data'),
     Output('playlist-url-store', 'data')],
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
            songs_list, artists_list, urls_list = [], [], []
            for recommendation in login_user_playlist:
                song = session.query(SpotifyData).filter_by(song_id=recommendation.song_id).first()
                if song:
                    songs_list.append(song.song_name)
                    artists_list.append(song.artist_name)
                    urls_list.append(song.song_id)
            session.close()
            return songs_list, artists_list, urls_list

    raise PreventUpdate


@dash.callback(
    Output('user-playlist-container', 'children'),
    [Input('playlist-song-store', 'data'),
     Input('playlist-artist-store', 'data'),
     Input('playlist-url-store', 'data')]
)
def update_user_playlist(songs_list, artists_list, urls_list):
    if songs_list and artists_list and urls_list:
        list_items = []
        base_url = "https://open.spotify.com/track/"
        for song, artist, url in zip(songs_list, artists_list, urls_list):
            track_url = base_url + url
            item = html.Li([
                html.A(song, href=track_url, target="_blank", className="song-name"),
                html.Div(artist, className="song-artist")
            ])
            list_items.append(item)
        return html.Ol(list_items)
    raise PreventUpdate



@callback(
    Output("user-attribute-radar-chart", "figure"),
    Input("song-selecting-dropdown", "data")
)