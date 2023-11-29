import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base

# Database setup
engine = create_engine('sqlite:///music_system.sqlite')
Base = declarative_base()


# Define the data model
class Users(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    sex = Column(String)
    age = Column(Integer)
    profile_pic = Column(String)  # Path to profile picture


class UserSongs(Base):
    __tablename__ = 'user_songs'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    song_id = Column(String, ForeignKey('spotify_data.song_id'))
    listening_count = Column(Integer)


class UserFriends(Base):
    __tablename__ = 'user_friends'
    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey('users.user_id'))
    friend_id = Column(String, ForeignKey('users.user_id'))


class SpotifyData(Base):
    __tablename__ = 'spotify_data'
    song_id = Column(String, primary_key=True)
    song_name = Column(String, nullable=False)
    artist_id = Column(String)
    artist_name = Column(String)
    year = Column(String)
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
    __tablename__ = 'data_by_year'
    id = Column(Integer, primary_key=True)
    year = Column(String)
    valence = Column(Float)
    acousticness = Column(Float)
    danceability = Column(Float)
    energy = Column(Float)
    instrumentalness = Column(Float)
    liveness = Column(Float)
    speechiness = Column(Float)
    popularity = Column(Integer)


Base.metadata.create_all(engine)


def initialize_user_database(document_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    # Load user data from CSV
    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        # Check if user already exists
        existing_user = session.query(Users).filter_by(user_id=row['user_id']).first()
        profile_pic_path = f"assets/profile_pics/{row['user_id']}.png"

        if existing_user:
            # Update existing user
            existing_user.first_name = row['first_name']
            existing_user.last_name = row['last_name']
            existing_user.sex = row['sex']
            existing_user.age = row['age']
            existing_user.profile_pic = profile_pic_path
        else:
            new_user = Users(
                user_id=row['user_id'],
                first_name=row['first_name'],
                last_name=row['last_name'],
                sex=row['sex'],
                age=row['age'],
                profile_pic=profile_pic_path
            )
            session.add(new_user)
    session.commit()
    session.close()
    print("User database successfully loaded.")


def initialize_spotify_database(document_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(SpotifyData).filter_by(song_id=row["song_id"]).first()
        if not existing_record:
            new_record = SpotifyData(
                song_id=row['song_id'],
                song_name=row['song_name'],
                artist_id=row['artist_id'],
                artist_name=row['artist_name'],
                year=row['year'],
                valence=row['valence'],
                acousticness=row['acousticness'],
                danceability=row['danceability'],
                energy=row['energy'],
                instrumentalness=row['instrumentalness'],
                liveness=row['liveness'],
                speechiness=row['speechiness'],
                genre=row['genre'],
                popularity=row['popularity']
            )
            session.add(new_record)
        else:
            pass
    session.commit()
    session.close()
    print("Spotify database successfully loaded.")


def initialize_year_database(document_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(DataByYear).filter_by(id=row["id"]).first()
        if not existing_record:
            new_record = DataByYear(
                id=row['id'],
                year=row['year'],
                valence=row['valence'],
                acousticness=row['acousticness'],
                danceability=row['danceability'],
                energy=row['energy'],
                instrumentalness=row['instrumentalness'],
                liveness=row['liveness'],
                speechiness=row['speechiness'],
                popularity=row['popularity']
            )
            session.add(new_record)
        else:
            pass
    session.commit()
    session.close()
    print("Year database successfully loaded.")


def initialize_user_songs_database(document_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    with session.no_autoflush:
        for index, row in df.iterrows():
            existing_record = session.query(UserSongs).filter_by(id=row["id"]).first()
            if not existing_record:
                new_record = UserSongs(
                    id=row['id'],
                    user_id=row['user_id'],
                    song_id=row['song_id'],
                    listening_count=row['listening_count']
                )
                session.add(new_record)
            else:
                pass
    session.commit()
    session.close()
    print("UserSongs database successfully loaded.")


def initialize_user_friends_database(document_path):
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv(document_path)

    for index, row in df.iterrows():
        existing_record = session.query(UserFriends).filter_by(user_id=row["user_id"],
                                                               friend_id=row["friend_id"]).first()
        if not existing_record:
            new_record = UserFriends(
                id=row['id'],
                user_id=row['user_id'],
                friend_id=row['friend_id']
            )
            session.add(new_record)
        else:
            pass
    session.commit()
    session.close()
    print("UserFriends database successfully loaded.")


if __name__ == "__main__":
    path1 = "../data/users.csv"
    path2 = "../data/spotify_data.csv"
    path3 = "../data/data_by_year.csv"
    path4 = "../data/user_songs.csv"
    path5 = "../data/user_friends.csv"
    initialize_user_database(path1)
    initialize_spotify_database(path2)
    initialize_year_database(path3)
    initialize_user_songs_database(path4)
    initialize_user_friends_database(path5)
