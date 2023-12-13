"""
Landing page for Spotify Music Exploration/Recommendation System.

This page serves as the entry point of the web application: it includes a CTA
button directing users to the "Explore" page.
"""

# Import packages
from dash import html, register_page

from utils.page_template import portfolio_wrapper

# Register the page
register_page(__name__, path="/", title="Spotify Music Recommendation System")

# Landing Page
landing_page = \
    html.Div([
        # Landing Page
        html.Div([
            # Headline
            html.H1(
                "Spotify Music Exploration + Recommendation System",
                className="landing-headline"
            ),

            # Button
            html.A(
                "Start Your Journey",
                href="/explore",
                className="start-button"
            ),
        ], className="landing-page"),
    ])

# Page Layout
layout = \
    portfolio_wrapper(
        landing_page
    )
