from dash import dcc, register_page, html

from utils.pages.recom.callbacks import *
from utils.page_template import portfolio_wrapper

register_page(__name__, path="/reco", title='Your Playlist - Spotify Music Recommendation System')

user_info_display = \
    html.Div([
        html.Div(id='user-profile-container'),
    ],
        style={'border-bottom': 'solid black 1px', 'display': 'grid', 'grid-template-columns': '600px auto',
               'height': '580px',
               'grid-auto-flow': 'row'}
    )

recommended_songs = \
    html.Div([
        html.Div([
            html.Div(style={'height': '100px'}),
            html.Span('Your recommended songs:',
                      style={
                          'width': '500px',
                          'font-size': '40px',
                          'font-weight': '600',
                          'height': 'auto',
                          'font-family': 'ultraboldFont'
                      }),
            html.P(
                'Gene expression profiling has been successfully used to classify different types of tumours such as '
                'breast, melanoma, lung and other. However, it is difficult to combine the insights for these studies '
                'into a more coherent and meaningful analysis that guide the next research step and could result in a '
                'quicker diagnosis, development of novel drugs or personalized therapies.',
                style={
                    'text-align': 'justify',
                    'text-justify': 'inter-word',
                    'font-family': 'roboto-light',
                }
            ),
            html.Div(style={'height': '100px'}),
            html.Div(
                html.H1("Your music style:",
                        style={
                            'font-family': 'regularFont',
                            'font-size': '40px'}),
                style={
                    'height': '100px',
                    'display': 'flex',
                    'align-items': 'flex-end'}
            )
        ],
            style={'display': 'grid', 'padding-left': '50px'}),
        html.Img(src='assets/genomic_analysis/stock-3.png',
                 # make it in the middle
                 style={'display': 'grid',
                        'margin-left': 'auto',
                        'margin-right': 'auto',
                        'padding-top': '100px',
                        'padding-bottom': '20px'}
                 )
    ],
        style={'border-bottom': 'solid black 1px', 'display': 'grid', 'grid-template-columns': '600px auto',
               'height': '580px',
               'grid-auto-flow': 'row'}
    )
# User profile page layout
logout_button = dcc.Link(
    html.Button("Logout", id="logout-button",
                style={'margin-top': '20px',
                       'height': '40px',
                       'padding': '10px 20px',
                       'font-size': '20px',
                       'font-weight': '600',
                       'display': 'inline-block'}),
    href="/"
)

layout = \
    portfolio_wrapper(
        user_info_display,
        recommended_songs,
        logout_button
    )
