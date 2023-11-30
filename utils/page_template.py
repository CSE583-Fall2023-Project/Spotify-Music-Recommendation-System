from dash import html, dcc


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

