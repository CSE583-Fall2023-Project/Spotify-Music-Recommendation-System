"""
Standard page template for the Spotify Music Exploration/Recommendation System.

This module defines a function to wrap given content into a standard layout,
which includes a navigation bar providing links to different pages of the app.
"""

# Import packages
from dash import html, dcc

# Define portfolio_wrapper function for consistent page layout
def portfolio_wrapper(*BODY):
    """
    Wraps the given page content with a standard navigation bar layout.

    Arguments:
        *body: Variable length argument list of Dash components to be wrapped.

    Returns a Dash HTML Div element containing the wrapped content.
    """
    return \
        html.Div([
            # Header
            html.Div(
                html.Div([
                    html.Div(
                        # Navigation Bar
                        html.Nav([
                            html.Ul([
                                html.Li(dcc.Link("Home", href="/")),
                                html.Li(dcc.Link("About", href="/about")),
                                html.Li(dcc.Link("Explore", href="/explore#01-music-trend=")),
                                html.Li(dcc.Link("Your Playlist", href="/login")),
                            ])
                        ], className="nav-bar")
                    ),
                ],
                )
            ),
            html.Div([*BODY],
                     id="page-body-id",
                     ),
        ],
            id="main-page-content",
        )
