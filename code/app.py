# app.py
"""
To launch the app, type command "python app.py" in terminal
Then navigate to the http link
"""

# Import packages
import pandas as pd
import plotly.express as px
import dash
from dash import Dash, dcc, html, Output, Input, callback


# Initialize the app
app = Dash(__name__, 
           use_pages = True, 
           external_stylesheets = ["assets/style.css"])


# Define the app layout and components
app.layout = html.Div([
    # Landing Page
    html.Div([
        # Navigation Bar
        html.Nav([
            html.Ul([
                html.Li(dcc.Link("Home", href = "/")),
                html.Li(dcc.Link("About", href = "/about")),
                html.Li(dcc.Link("Explore", href = "/explore#01-music-trend=")),
                html.Li(dcc.Link("Recommendations", href = "/reco")),
            ])
        ], className = "nav-bar")
    ]),
    dash.page_container
])


# Run the app
if __name__ == "__main__":
    app.run_server(debug = True)