"""
Unit Testing for User Recommendation System in Spotify Music Exploration/Recommendation System.

This module provides unit tests for the recommendation system, ensuring that
users receive accurate playlist recommendations based on their listening history.
Tests include verifying playlist lengths, user existence, and data integrity.
"""

import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.pages.recom.playlist import fetch_user_playlist
from utils.database import Base, Users, UserRecommendation, SpotifyData


class TestRecommendation(unittest.TestCase):
    """
    A TestCase class for testing the recommendation functionalities.

    This class includes methods for setting up a test database environment,
    adding test users and their music preferences, and defining various test
    cases for the recommendation functionalities.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up an in-memory SQLite database for testing recommendation features.

        This method initializes a SQLite in-memory database and prepares
        table schemas for Users, UserRecommendation, and SpotifyData.
        """
        cls.engine = create_engine("sqlite:///:memory:")  # Use in-memory database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Prepare the database session and add test data before each test.

        This method initializes a new database session and adds a test user
        along with their music preferences before each test case is run.
        """
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
        """
        Add test user data and their music preferences to the database.

        This method clears any existing records and inserts a predefined user
        and their top 10 song recommendations for testing the recommendation system.
        """
        # Clear tables first to avoid integrity errors
        self.session.query(UserRecommendation).delete()
        self.session.query(SpotifyData).delete()
        self.session.query(Users).delete()

        valid_user = Users(
            user_id="user_id_1",
            first_name="Honorable",
            last_name="User",
        )
        self.session.add(valid_user)

        # Add UserRecommendations and SpotifyData
        for i in range(1, 11):
            song_id = f"song_id_{i}"
            self.session.add(UserRecommendation(
                user_id="user_id_1",
                song_id=song_id,
                rank=i
            ))
            self.session.add(SpotifyData(
                song_id=song_id,
                song_name=f"Song {i}",
                artist_name=f"Singer {i}"
            ))

        self.session.commit()

    def tearDown(self):
        """
        Rollback the database transaction after each test.

        This method ensures database isolation between tests by rolling back
        any changes made during the test execution.
        """
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_fetch_user_playlist_length(self):
        """
        Test fetching the playlist length for a valid user.

        This test verifies that fetch_user_playlist function returns a playlist
        of the correct length for a valid user.
        """
        # Call fetch_user_playlist with a mocked session
        songs_list, artists_list, _ = fetch_user_playlist(
            "user_id_1", 
            session=self.session
        )
        # Assertions
        self.assertEqual(len(songs_list), 10)
        self.assertEqual(len(artists_list), 10)
        self.assertEqual(len(songs_list), len(artists_list))

    def test_nonexistent_user(self):
        """
        Test playlist retrieval for a non-existent user.

        This test checks if fetch_user_playlist returns empty lists for a user
        that does not exist in the database.
        """
        # Test behavior for a non-existent user
        songs_list, artists_list, _ = fetch_user_playlist(
            "user_id_nonexistent",
            session=self.session
        )
        self.assertEqual(songs_list, [])
        self.assertEqual(artists_list, [])

    def test_data_integrity(self):
        """
        Test the integrity of data in fetched playlists.

        This test ensures that the fetch_user_playlist function retrieves the
        correct song and artist names that match the test data for a valid user.
        """
        # Check if the fetched data matches the expected results
        songs_list, artists_list, _ = fetch_user_playlist("user_id_1", session=self.session)
        expected_songs = ["Song 1", "Song 2", "Song 3", "Song 4", "Song 5",
                          "Song 6", "Song 7", "Song 8", "Song 9", "Song 10"]
        expected_artists = ["Singer 1", "Singer 2", "Singer 3", "Singer 4", "Singer 5",
                            "Singer 6", "Singer 7", "Singer 8", "Singer 9", "Singer 10"]
        # No artist data in the test setup, so artists_list is expected to be empty
        self.assertEqual(songs_list, expected_songs)
        self.assertEqual(artists_list, expected_artists)


if __name__ == "__main__":
    unittest.main()
