from dash import html, dcc
import dash_bootstrap_components as dbc


def portfolio_wrapper(*BODY):
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
                     id='page-body-id',
                     ),
        ],
            id='main-page-content',
        )

# # Define the app layout and components
# app.layout = html.Div([
#     # Landing Page
#     html.Div([
#         # Navigation Bar
#         html.Nav([
#             html.Ul([
#                 html.Li(dcc.Link("Home", href = "/")),
#                 html.Li(dcc.Link("About", href = "/about")),
#                 html.Li(dcc.Link("Explore", href = "/explore#01-music-trend=")),
#                 html.Li(dcc.Link("Recommendations", href = "/reco")),
#             ])
#         ], className = "nav-bar")
#     ]),
#     dash.page_container
# ])
