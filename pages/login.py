from dash import dcc, register_page
from utils.pages.login.callbacks import *
from utils.page_template import portfolio_wrapper

register_page(__name__, path="/login", title='Login - Spotify Music Recommendation System')

login_page = html.Div([
    # Login header layout
    html.Div(id="login-header", children=[
        html.Div([
            html.H2('Get your music profile with your next 10 favorite songs!',
                    className="section-title"),
            html.H3("Type in your name and it will magically happen!",
                    className="section-subtitle"),
            html.Hr(className="section-divider"),
        ]),
    ], className="login-page"),

    # Login window layout
    html.Div(id="login-window", children=[
        html.Div(style={'height': '100px'}),  # Spacer
        html.Div([
            # Title for the login section
            html.Span('User Login',
                      style={
                          'font-size': '50px',
                          'font-weight': '700',
                          'font-family': 'Gill Sans',
                          'color': 'white'
                      }),

            # Input fields for first and last name
            html.Div([
                dcc.Input(id='first-name', type='text', placeholder='First Name',
                          style={'margin-right': '10px', 'margin-top': '25px', 'height': '40px', 'font-size': '20px'}),
                dcc.Input(id='last-name', type='text', placeholder='Last Name',
                          style={'margin-top': '25px', 'height': '40px', 'font-size': '20px'})
            ], style={'display': 'flex'}),

            # Login button
            dcc.Link(
                id="login-link",
                children=html.Button('Login', id='login-button',
                                     n_clicks=0,
                                     className='login-button'),
                href="/login"
            ),
            # Placeholder for login output message
            html.Div(
                id='login-output',
                style={'margin-top': '20px'}
            )
        ], style={'padding-right': '50px', 'padding-top': '20px'}),  # Content styling
    ], className="login-window")
])

layout = portfolio_wrapper(login_page)
