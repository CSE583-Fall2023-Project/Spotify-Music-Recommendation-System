# about.py

"""
About page for the Spotify Music Exploration/Recommendation System. 

This page provides an overview of the system, its features and functionalities.
For more information or to view the source code, visit the GitHub repository:
https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System.
"""

import dash
from dash import dcc, html, register_page

from utils.page_template import portfolio_wrapper

# Register the page
register_page(__name__, path = "/about", title="About")

repo = "https://github.com/CSE583-Fall2023-Project/Spotify-Music-Recommendation-System"

about_page = html.Div([
    # About Page
    html.Div(id="about-page", children=[
        # Title and subtitle
        html.Div([
            html.H2("About the Project",
                    className="section-title"),
            html.H3("The Spotify Music Exploration/Recommendation System",
                    className="section-subtitle"),
            html.Hr(className="section-divider")
        ], className="about-page-title"),

        # Content
        html.Div([
            html.P("This system is designed to help users explore and discover music on Spotify. "
                   "Using various data visualization and recommendation techniques, it aims to "
                   "enhance the user's music listening experience."),
            html.P("To learn more about how this system works, contribute to its development, "
                   "or report issues, please visit our GitHub repository."),
            html.A([
                html.Img(src="assets/github-logo.png", className="github-icon"), 
            ], href=repo, target="_blank")
        ], className="about-page-content"),
    ])
], className="about-page")

layout = \
    portfolio_wrapper(
        about_page
    )