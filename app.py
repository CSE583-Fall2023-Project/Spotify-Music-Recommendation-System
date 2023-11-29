# app.py
"""
To launch the app, type command "python app.py" in terminal
Then navigate to the http link
"""

# Import packages
import dash
from dash import Dash, dcc, html

PORT = 5000
ADDRESS = '127.0.0.1'

# Initialize the app
app = Dash(__name__,
           external_stylesheets=["assets/style.css"],
           title='Spotify Music Recommendation System',
           use_pages=True
           )

app._favicon = 'spotify.ico'

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-info-store'),
    dash.page_container,
])

# Run the app
if __name__ == "__main__":
    app.run_server(
        port=PORT,
        host=ADDRESS,
        debug=True
    )

