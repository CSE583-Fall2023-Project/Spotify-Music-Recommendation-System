"""
Database setup for the Spotify Music Exploration/Recommendation System.

This module sets up a relational database and defines data models for users and songs.
It includes functions for extracting data from CSVs into corresponding tables.
The populated database can be accessed through the "spotipy_db.sqlite" file,
the central data store of the application.
"""

# Import packages
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

from utils.pages.recom.model import RecommendationModel


# Database setup
engine = create_engine("sqlite:///spotipy_db.sqlite")
Base = declarative_base()


# Define the data model
class Users(Base):
    """
    Represents the Users table in the database.
    Contains dummy data for 2000 users.

    Constraints:
        PRIMARY KEY constraint on "user_id";
        NOT NULL constraint on "first_name" and "last_name".
    """
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(String)
    age = Column(Integer)
    profile_pic = Column(String)  # Path to profile picture


class UserSongs(Base):
    """
    Represents the UserSongs table in the database.
    Associative entity between Users and SpotifyData; contains dummy data for 
    10,000 user-song combinationss.

    Constraints:
        PRIMARY KEY constraint on "id";
        FOREIGN KEY constraint on "user_id" and "song_id".
    """
    __tablename__ = "user_songs"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    song_id = Column(String, ForeignKey("spotify_data.song_id"))
    listening_count = Column(Integer)


class UserFriends(Base):
    """
    Represents the UserFriends table in the database.
    Contains 24,000 generated (user_i, user_j) pairs.

    Constraints:
        PRIMARY KEY constraint on "id";
        FOREIGN KEY constraint on "user_id", "friend_id".
    """
    __tablename__ = "user_friends"
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    friend_id = Column(String, ForeignKey("users.user_id"))


class SpotifyData(Base):
    """
    Represents the SpotifyData table in the database.
    Contains over 170,000 songs released from 1921 to 2020 on Spotify, including
    metadata, audio features and popularity metrics for each track.

    Constraints:
        PRIMARY KEY constraint on "song_id";
        NOT NULL constraint on "song_name".
    """
    __tablename__ = "spotify_data"
    song_id = Column(String, primary_key=True)
    song_name = Column(String, nullable=False)
    artist_id = Column(String)
    artist_name = Column(String)
    year = Column(Integer)
    valence = Column(Float)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    speechiness = Column(Float)
    genre = Column(String)
    popularity = Column(Integer)


class DataByYear(Base):
    """
    Represents the DataByYear table in the database.
    Contains aggregated song data by year.

    Constraints:
        PRIMARY KEY constraint on "id".
    """
    __tablename__ = "data_by_year"
    id = Column(Integer, primary_key=True)
    year = Column(Integer)
    valence = Column(Float)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    speechiness = Column(Float)
    popularity = Column(Integer)


class UserRecommendation(Base):
    """
    Represents the UserRecommendation table in the databade.
    Contains song recommendations for users.

    Constraints:
        PRIMARY KEY constraint on "id", an auto-incremented surrogate key;
        FOREIGN KEY constraint on "user_id" and "song_id".
    """
    __tablename__ = "user_recommendations"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    song_id = Column(String, ForeignKey("spotify_data.song_id"))
    rank = Column(Integer)


# Create all tables in the database
Base.metadata.create_all(engine)


# Load data into databases
def initialize_user_database(document_path):
    """
    Initializes and populates the Users database from given CSV file.
    Updates information for existing users and inserts new records for new users.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        document_path (str): Path to the CSV file containing user data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load user data from CSV
    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        # Check if user already exists
        existing_user = session.query(Users).filter_by(user_id=row["user_id"]).first()
        profile_pic_path = f"assets/profile_pics/{row['user_id']}.png"

        if existing_user:
            # Update existing user
            existing_user.first_name = row["first_name"]
            existing_user.last_name = row["last_name"]
            existing_user.sex = row["sex"]
            existing_user.age = row["age"]
            existing_user.profile_pic = profile_pic_path
        else:
            new_user = Users(
                user_id=row["user_id"],
                first_name=row["first_name"],
                last_name=row["last_name"],
                sex=row["sex"],
                age=row["age"],
                profile_pic=profile_pic_path
            )
            session.add(new_user)
    try:
        session.commit()
        print("Users database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


def initialize_spotify_database(document_path):
    """
    Initializes and populates the SpotifyData database from given CSV file.
    Inserts a new record if a song does not exist; otherwise leaves as is.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        document_path (str): Path to the CSV file containing spotify song data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(SpotifyData).filter_by(song_id=row["song_id"]).first()
        if not existing_record:
            new_record = SpotifyData(
                song_id=row["song_id"],
                song_name=row["song_name"],
                artist_id=row["artist_id"],
                artist_name=row["artist_name"],
                year=row["year"],
                valence=row["valence"],
                acousticness=row["acousticness"],
                danceability=row["danceability"],
                energy=row["energy"],
                instrumentalness=row["instrumentalness"],
                liveness=row["liveness"],
                speechiness=row["speechiness"],
                genre=row["genre"],
                popularity=row["popularity"]
            )
            session.add(new_record)
        else:
            pass
    try:
        session.commit()
        print("Spotify database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


def initialize_year_database(document_path):
    """
    Initializes and populates the DataByYear database from given CSV file.
    Inserts a new record if a year does not exist; otherwise leaves as is.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        document_path (str): Path to the CSV file containing aggregated year data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(DataByYear).filter_by(id=row["id"]).first()
        if not existing_record:
            new_record = DataByYear(
                id=row["id"],
                year=row["year"],
                valence=row["valence"],
                acousticness=row["acousticness"],
                danceability=row["danceability"],
                energy=row["energy"],
                instrumentalness=row["instrumentalness"],
                liveness=row["liveness"],
                speechiness=row["speechiness"],
                popularity=row["popularity"]
            )
            session.add(new_record)
        else:
            pass
    try:
        session.commit()
        print("Year database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


def initialize_user_songs_database(document_path):
    """
    Initializes and populates the UserSongs database from given CSV file.
    Inserts a new record if a user-song combination does not exist; otherwise leaves as is.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        document_path (str): Path to the CSV file containing user-song data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    with session.no_autoflush:
        for index, row in df.iterrows():
            existing_record = session.query(UserSongs).filter_by(id=row["id"]).first()
            if not existing_record:
                new_record = UserSongs(
                    id=row["id"],
                    user_id=row["user_id"],
                    song_id=row["song_id"],
                    listening_count=row["listening_count"]
                )
                session.add(new_record)
            else:
                pass
    try:
        session.commit()
        print("UserSongs database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


def initialize_user_friends_database(document_path):
    """
    Initializes and populates the UserFriends database from given CSV file.
    Inserts a new record if a user-friend pair does not exist; otherwise leaves as is.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        document_path (str): Path to the CSV file containing user-friends data.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(UserFriends).filter_by(user_id=row["user_id"],
                                                               friend_id=row["friend_id"]).first()
        if not existing_record:
            new_record = UserFriends(
                id=row["id"],
                user_id=row["user_id"],
                friend_id=row["friend_id"]
            )
            session.add(new_record)
        else:
            pass
    try:
        session.commit()
        print("UserFriends database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


def initialize_user_recommendations_database(top_n_playlist):
    """
    Initializes and populates the UserRecommendation database from given CSV file.
    Inserts recommendations from top_n_playlist.
    Commits all changes to the database once all records are processed; rollback
    in case of exceptions.

    Arguments:
        top_n_playlist (dict): A dictionary with user_id as key and recommended
        song tuples (song_id, rank) as values.
    """
    Session = sessionmaker(bind=engine)
    session = Session()

    for user_id, song_list in top_n_playlist.items():
        for rank, (song_id, _) in enumerate(song_list, start=1):
            recommendation = UserRecommendation(user_id=user_id, song_id=song_id, rank=rank)
            session.add(recommendation)
    try:
        session.commit()
        print("UserRecommendation database successfully loaded.")
    except Exception as excep:
        print(f"An error occurred: {excep}")
        session.rollback()
    finally:
        session.close()


# Main function for database initialization
if __name__ == "__main__":
    # File paths for data sources
    PATH1 = "../data/users.csv"
    PATH2 = "../data/spotify_data.csv"
    PATH3 = "../data/data_by_year.csv"
    PATH4 = "../data/user_songs.csv"
    PATH5 = "../data/user_friends.csv"

    # Initialize databases with data from given CSV files
    initialize_user_database(PATH1)
    initialize_spotify_database(PATH2)
    initialize_year_database(PATH3)
    initialize_user_songs_database(PATH4)
    initialize_user_friends_database(PATH5)

    # Initializes recommendation table from generated recommendations
    model = RecommendationModel(PATH4, PATH5)
    model.train()
    predictions = model.predict()
    top_n_playlist = model.get_top_n_songs(predictions, 10)
    initialize_user_recommendations_database(top_n_playlist)
