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

# Create session and connect to database
Session = sessionmaker(bind=engine)
session = Session()

# Determine the range and marks for the slider
min_year = session.query(func.min(DataByYear.year)).scalar()
max_year = session.query(func.max(DataByYear.year)).scalar()
min_year = int(float(min_year))
max_year = int(float(max_year))


# Create decades list
decades = list(range(min_year + (10 - min_year % 10), max_year + 1, 10))
decades = [min_year] + decades if min_year not in decades else decades
decades += [max_year] if max_year not in decades else []

# Create marks
marks = {int(year): {"label": str(year)} for year in decades}

# Songs and attributes
attributes = ["acousticness", "danceability", "energy", "instrumentalness",
              "liveness", "speechiness", "valence"]

# Query to select distinct song names ordered by popularity in descending order
sorted_songs_query = session.query(SpotifyData.song_name). \
    distinct().order_by(desc(SpotifyData.popularity))

sorted_songs = [song[0] for song in sorted_songs_query.all()]


# Add controls to build the interaction
# Visualization #1
@callback(
    Output(component_id="attribute-trend-line-chart", component_property="figure"),
    Input(component_id="attribute-checklist", component_property="value"),
    Input(component_id="year-range-slider", component_property="value")
)
def update_attribute_trend(selected_attributes, selected_years):
    filtered_data_query = session.query(DataByYear).filter(
        and_(
            DataByYear.year >= selected_years[0],
            DataByYear.year <= selected_years[1]
        )
    )

    # Extract the data from the query
    filtered_data = pd.read_sql(filtered_data_query.statement, session.bind)

    # Plotting with Plotly
    fig = px.line(filtered_data, x="year", y=selected_attributes)

    # Update plot layout
    fig.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(family="Gill Sans, Arial, sans-serif",
                  color="#f2f2f2")
    )
    return fig


# Visualization #2
@callback(
    Output("song-attribute-radar-chart", "figure"),
    Input("song-selecting-dropdown", "value")
)
def update_song_attributes(selected_song):
    if selected_song:
        # Query to get data for the selected song
        song_data_query = session.query(SpotifyData).filter(
            and_(
                SpotifyData.song_name == selected_song
            ))
        song_data_df = pd.read_sql(song_data_query.statement, song_data_query.session.bind)

        if not song_data_df.empty:
            song_data = song_data_df.iloc[0]
            radar_data = pd.DataFrame({
                "Attribute": attributes,
                "Value": [song_data[attr] for attr in attributes]
            })
            fig = px.line_polar(
                radar_data,
                r="Value",
                theta="Attribute",
                line_close=True)
            fig.update_traces(
                fill="toself",
                fillcolor="rgba(29, 185, 84, 0.5)",
                line=dict(color="#1db954")
            )
            fig.update_layout(
                plot_bgcolor="#121212",
                paper_bgcolor="#121212",
                font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14)
            )
            return fig
        else:
            # Return an empty plot if no data is found
            return empty_radar_plot()

    else:
        # Return an empty plot if no song is selected
        return empty_radar_plot()


def empty_radar_plot():
    fig = px.line_polar(
        r=[0, 0, 0, 0, 0, 0, 0],
        theta=attributes
    )
    fig.update_layout(
        plot_bgcolor="#121212",
        paper_bgcolor="#121212",
        font=dict(family="Gill Sans, Arial, sans-serif", color="#1db954", size=14)
    )
    return fig


session.close()
