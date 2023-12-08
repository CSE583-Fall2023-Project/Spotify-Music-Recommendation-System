# login.py

"""
Login Page for the Spotify Music Exploration/Recommendation System. 

Authenticates users by taking their first and last name as input then 
performing user match to verify the existence of the user in the system's 
database.  

Once authenticated, users will proceed to their personalized music profile.
"""

# Import packages
from dash import dcc, html, register_page
from utils.pages.login.callbacks import *
from utils.page_template import portfolio_wrapper

# Register the page
register_page(__name__, path="/login", title="Login - Spotify Music Recommendation System")

# Login Page
login_page = html.Div([
    # Login Header
    html.Div(id="login-header", children=[
        html.Div([
            html.H2("Get your music profile with your next 10 favorite songs!",
                    className="section-title"),
            html.H3("Type in your name and it will magically happen!",
                    className="section-subtitle"),
            html.Hr(className="section-divider"),
        ]),
    ], className="login-page"),

    # Login Window
    html.Div([
        html.Div([
            # Login Section Title
            html.P("User Login", className="login-heading"),

            # Input fields for first and last name
            html.Div([
                dcc.Input(id="first-name", type="text", placeholder="First Name",
                        className="first-name-input"),
                dcc.Input(id="last-name", type="text", placeholder="Last Name",
                        className="last-name-input"),
            ]),

            # Login Button
            dcc.Link(
                id="login-link",
                children=html.Button("Login", id="login-button",
                                    n_clicks=0,
                                    className="login-button"),
                href="/login"
            ),
            # Placeholder for login output message
            html.Div(id="login-output", className="login-output")
        ], className="login-window")
    ], className="login-window-container")
])

# Page Layout
layout = portfolio_wrapper(login_page)
