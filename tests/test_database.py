"""
Unit Testing for Database Interactions in Spotify Music Exploration/Recommendation System.

This module contains unit tests for database interactions, specifically testing
the functionality of adding and retrieving data from the Users and SpotifyData
tables. It ensures that data is correctly inserted and can be fetched accurately.
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.database import Base, Users, SpotifyData


class TestDatabase(unittest.TestCase):
    """
    A TestCase class for testing database interactions.

    This class contains methods to set up a test database, add test data,
    and define various test cases for validating the Users and SpotifyData
    tables' functionality.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up an in-memory SQLite database for testing.

        This method is called once before running the first test. It creates
        a new SQLite in-memory database and sets up the necessary table schemas.
        """
        # Use in-memory database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Prepare the database session and add test data before each test.

        This method is called before each test function execution. It starts a
        new database session and inserts test data into the database.
        """
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
        """
        Add test data to the database.

        This method clears existing records and adds predefined Users and
        SpotifyData records to the database for testing purposes.
        """
        # Clear tables first to avoid integrity errors
        self.session.query(SpotifyData).delete()
        self.session.query(Users).delete()

        # Add a valid user and song to the database
        valid_user = Users(
            user_id="001aa",
            first_name="Cardi",
            last_name="B",
            sex="F",
            age=30,
            profile_pic="assets/profile_pics/001aa.png"
        )
        self.session.add(valid_user)

        valid_song = SpotifyData(
            song_id='7DjCRhhFo9PPzca1BjMLcf',
            song_name='Long Live',
            artist_id='349a6f757a',
            artist_name='Taylor Swift',
            year='2010',
            valence=0.142,
            acousticness=0.036,
            danceability=0.418,
            energy=0.68,
            instrumentalness=7.59e-05,
            liveness=0.114,
            speechiness=0.0347,
            genre='dance pop, pop, pop dance, post-teen pop',
            popularity=53
        )
        self.session.add(valid_song)
        self.session.commit()

    def tearDown(self):
        """
       Rollback the database transaction after each test.

       This method is called after each test function execution to ensure
       database isolation between tests by rolling back the current transaction.
       """
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_adding_valid_user_to_database(self):
        """
        Test adding a valid user record to the database.

        This test ensures that a valid Users record can be added and retrieved
        accurately from the database.
        """
        user = self.session.query(Users).filter_by(user_id="001aa").first()
        self.assertEqual(user.first_name, "Cardi")
        self.assertEqual(user.last_name, "B")
        self.assertEqual(user.sex, "F")
        self.assertEqual(user.age, 30)
        self.assertEqual(user.profile_pic, "assets/profile_pics/001aa.png")

    def test_adding_valid_song_to_database(self):
        """
        Test adding a valid song record to the database.

        This test verifies that a SpotifyData record can be inserted and
        correctly fetched from the database.
        """
        song = self.session.query(SpotifyData).\
            filter_by(song_id="7DjCRhhFo9PPzca1BjMLcf").first()
        self.assertEqual(song.song_name, "Long Live")
        self.assertEqual(song.artist_id, "349a6f757a")
        self.assertEqual(song.artist_name, "Taylor Swift")
        self.assertEqual(song.year, 2010)
        self.assertEqual(song.valence, 0.142)
        self.assertEqual(song.acousticness, 0.036)
        self.assertEqual(song.danceability, 0.418)
        self.assertEqual(song.energy, 0.68)
        self.assertEqual(song.instrumentalness, 7.59e-05)
        self.assertEqual(song.liveness, 0.114)
        self.assertEqual(song.speechiness, 0.0347)
        self.assertEqual(song.genre, "dance pop, pop, pop dance, post-teen pop")
        self.assertEqual(song.popularity, 53)


if __name__ == '__main__':
    unittest.main()
