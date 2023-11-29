# home.py
import dash
from dash import html

from utils.page_template import portfolio_wrapper


dash.register_page(__name__, path="/", title='Spotify Music Recommendation System')

landing_page = \
    html.Div([
        # Landing Page
        html.Div([
            # Headline
            html.H1("Spotify Music Exploration + Recommendation System",
                    className="landing-headline"),

            # Button
            html.A("Start Your Journey",
                   href="/explore",
                   className="start-button"),
        ], className="landing-page"),
    ])

layout = \
    portfolio_wrapper(
        landing_page
    )
