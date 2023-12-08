from dash.exceptions import PreventUpdate
from sqlalchemy.orm import sessionmaker
from dash import Output, Input, State, html
import dash

from utils.database import Users, engine

# Create a session maker bound to your engine
Session = sessionmaker(bind=engine)

# User authentciation function
def check_user(first_name, last_name):
    session = Session()
    user = session.query(Users).filter_by(first_name=first_name, last_name=last_name).first()
    print(user)
    session.close()
    if user:
        user_data = {
            'user_id': user.user_id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'sex': user.sex,
            'age': user.age,
            'profile_pic': user.profile_pic
        }
        return [True, user_data]
    return [False, None]


# Callback for Handling Login Attempts
@dash.callback(
    [Output('login-link', 'href'),
     Output('user-info-store', 'data'),
     Output('login-output', 'children')],
    Input('login-button', 'n_clicks'),
    [State('first-name', 'value'),
     State('last-name', 'value')]
)
def handle_login(n_clicks, first_name, last_name):
    if n_clicks:
        user_exists, user_data = check_user(first_name, last_name)
        if user_exists:
            # Redirect to the profile page and store user data
            print(user_data)
            return ["/reco", user_data, None]
        else:
            # Stay on the same page and show an error message
            return ["", dash.no_update, 
                    html.Div("User not found. Please check your name spelling and try again.")]
    raise PreventUpdate


@dash.callback(
    Output('user-profile-container', 'children'),
    [Input('user-info-store', 'data')]
)
def update_user_profile(user_data):
    if user_data:
        profile_pic_url = user_data['profile_pic']
        return html.Div([
            html.Div(
                html.Img(src=profile_pic_url, className="user-profile-image"),
                className="user-image-container"
            ),
            html.Div([
                html.P(f"{user_data['first_name']} {user_data['last_name']}", 
                    className="user-name"),
                html.P(f"Age: {user_data['age']} | Sex: {user_data['sex']}", className="user-detail"),
            ], className="user-detail-container")
        ], className="user-info-container")
    return PreventUpdate
