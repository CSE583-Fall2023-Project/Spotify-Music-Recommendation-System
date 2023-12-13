"""
Defines utility functions and Dash callbacks for the Login page.

This module contains utility and callback functions for authenticating users and
updating user profile upon successful login attempts.
"""

# Import packages
import dash
from dash import Output, Input, State, html
from dash.exceptions import PreventUpdate
from sqlalchemy.orm import sessionmaker

from utils.database import Users, engine

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)


# Function for user authentication
def check_user(first_name, last_name, session=None):
    """
    Performs user authentication based on user first and last name.

    Arguments:
        first_name (str): User's first name.
        last_name (str): User's last name.
        session: SQLAlchemy session (optional).

    Returns a list containing a boolean indicating whether user exists and a
    dict storing user data.    
    """
    own_session = False
    if session is None:
        session = Session()
        own_session = True

    user = session.query(Users).filter_by(first_name=first_name, last_name=last_name).first()
    if own_session:
        session.close()
    if user:
        user_data = {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "sex": user.sex,
            "age": user.age,
            "profile_pic": user.profile_pic
        }
        return [True, user_data]
    return [False, None]


# Callback function for handling login attempts
@dash.callback(
    [Output("login-link", "href"),
     Output("user-info-store", "data"),
     Output("login-output", "children")],
    Input("login-button", "n_clicks"),
    [State("first-name", "value"),
     State("last-name", "value")]
)
def handle_login(n_clicks, first_name, last_name, session=None):
    """
    Handles login attempts.  Authenticates user upon click; once authenticated,
    redirects user to personalized reco page.

    Arguments:
        n_clicks (int): 
        first_name (str): User's first name.
        last_name (str): User's last name.
        session: SQLAlchemy session (optional).
    
    Returns a list containing login link, user data, and login output message.
    """
    if session is None:
        session = Session()
    else:
        session = session
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            # Redirect to the profile page and store user data
            print(user_data)
            return ["/reco", user_data, None]
        # Stay on the same page and show an error message
        return ["", dash.no_update,
                html.Div("User not found. Please check your name spelling and try again.")]
    raise PreventUpdate


# Callback function for updating user profile
@dash.callback(
    Output("user-profile-container", "children"),
    [Input("user-info-store", "data")]
)
def update_user_profile(user_data, session=None):
    """
    Updates user profile upon successful login.

    Arguments:
        user_data (dict): A dictionary containing user data.
        session: SQLAlchemy session (optional).
    
    Returns a Dash component with updated user profile container.
    """
    if session is None:
        session = Session()
    else:
        session = session
    if user_data:
        profile_pic_url = user_data["profile_pic"]
        return html.Div([
            html.Div(
                html.Img(src=profile_pic_url, className="user-profile-image"),
                className="user-image-container"
            ),
            html.Div([
                html.P(
                    f"{user_data['first_name']} {user_data['last_name']}",
                    className="user-name"
                ),
                html.P(
                    f"Age: {user_data['age']} | Sex: {user_data['sex']}",
                    className="user-detail"
                ),
            ], className="user-detail-container")
        ], className="user-info-container")
    return PreventUpdate
