# utils/pages/explore/visuals.py

"""

"""

import pandas as pd
import plotly.express as px
from dash import callback, Output, Input
from sqlalchemy import func, desc, and_
from sqlalchemy.orm import sessionmaker
from plotly.graph_objects import Layout
from plotly.validator_cache import ValidatorCache

from utils.database import SpotifyData, DataByYear, engine


# Set up the SQLAlchemy session
Session = sessionmaker(bind=engine)

# Define global variables
attributes = ["acousticness", "danceability", "energy", "instrumentalness",
              "liveness", "speechiness", "valence"]


def get_min_max_years(session=None):
    """Retrieve the minimum and maximum years from DataByYear."""
    if session is not None:
        session = session
    else:
        session = Session()
    min_year = session.query(func.min(DataByYear.year)).scalar()
    max_year = session.query(func.max(DataByYear.year)).scalar()
    return int(float(min_year)), int(float(max_year))


def get_decades(min_year, max_year, session=None):
    """Create a list of decades based on the min and max years."""
    if session is not None:
        session = session
    else:
        session = Session()
    decades = list(range(min_year + (10 - min_year % 10), max_year + 1, 10))
    decades = [min_year] + decades if min_year not in decades else decades
    decades += [max_year] if max_year not in decades else []
    return decades


def get_sorted_songs(session=None):
    """Retrieve sorted song names based on popularity."""
    if session is not None:
        session = session
    else:
        session = Session()
    sorted_songs_query = session.query(SpotifyData.song_name). \
        distinct().order_by(desc(SpotifyData.popularity))
    return [song[0] for song in sorted_songs_query.all()]


def empty_radar_plot():
    """Create an empty radar plot."""
    fig = px.line_polar(r=[0, 0, 0, 0, 0, 0, 0], theta=attributes)
    fig.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14)
    )
    return fig


# Callbacks for Visualization #1
@callback(
    Output(component_id="attribute-trend-line-chart", component_property="figure"),
    Input(component_id="attribute-checklist", component_property="value"),
    Input(component_id="year-range-slider", component_property="value")
)
def update_attribute_trend(selected_attributes, selected_years):
    with Session() as session:
        filtered_data_query = session.query(DataByYear).filter(
            and_(
                DataByYear.year >= selected_years[0],
                DataByYear.year <= selected_years[1]
            )
        )
        # Extract the data from the query
        filtered_data = pd.read_sql(filtered_data_query.statement, session.bind)
        fig = px.line(filtered_data, x="year", y=selected_attributes)
        fig.update_layout(
            plot_bgcolor="#121212",
            paper_bgcolor="#121212",
            font=dict(
                family="Gill Sans, Arial, sans-serif", 
                color="#f2f2f2"
            )
        )
        fig.update_xaxes(
            showgrid=True,
            gridcolor='rgba(242, 242, 242, 0.5)',
            tickmode="linear",
            tick0="1920",
            dtick=10,
            tickformat=",d"
        )
        fig.update_yaxes(
            showgrid=True,
            zeroline=False,
            gridcolor='rgba(242, 242, 242, 0.5)'
        )
        return fig


# Visualization #2
@callback(
    Output("song-attribute-radar-chart", "figure"),
    Input("song-selecting-dropdown", "value")
)
def update_song_attributes(selected_song, session=None):
    if session is not None:
        session = session
    else:
        session = Session()
    if selected_song:
        song_data_query = session.query(SpotifyData).filter(
            and_(SpotifyData.song_name == selected_song)
        )
        song_data_df = pd.read_sql(song_data_query.statement, song_data_query.session.bind)
        if not song_data_df.empty:
            song_data = song_data_df.iloc[0]
            radar_data = pd.DataFrame({"Attribute": attributes,
                                       "Value": [song_data[attr] for attr in attributes]})
            fig = px.line_polar(radar_data,
                                r="Value",
                                theta="Attribute",
                                line_close=True)
            fig.update_traces(fill="toself",
                              fillcolor="rgba(29, 185, 84, 0.5)",
                              line=dict(color="#1db954"))
            fig.update_layout(plot_bgcolor="#121212",
                              paper_bgcolor="#121212",
                              font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14))
            return fig
        return empty_radar_plot()
    return empty_radar_plot()


# Execute setup functions
min_year, max_year = get_min_max_years()
decades = get_decades(min_year, max_year)
sorted_songs = get_sorted_songs()
marks = {int(year): {"label": str(year)} for year in decades}
