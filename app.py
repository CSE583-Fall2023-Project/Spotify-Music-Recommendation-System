# app.py

"""
Main app file for Spotify Music Exploration/Recommendation System.

To launch the app, type command "python app.py" in terminal,
then navigate to the http link (http://127.0.0.1:5000/).
"""

# Import packages
import dash
from dash import Dash, dcc, html

# Constants for port and address
PORT = 5000
ADDRESS = "127.0.0.1"

# Initialize the Dash app
app = Dash(
    __name__,
    external_stylesheets=["assets/style.css"],
    title="Spotify Music Recommendation System",
    use_pages=True
)

# Set browser tab icon
app._favicon = "spotify.ico"

# Define app layout
app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    dcc.Store(id="user-info-store"),
    dcc.Store(id="playlist-song-store"),
    dcc.Store(id="playlist-artist-store"),
    dash.page_container,
])

# Run the app
if __name__ == "__main__":
    app.run_server(port=PORT, host=ADDRESS, debug=True)
