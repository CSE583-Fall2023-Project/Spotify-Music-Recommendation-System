import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from utils.pages.recom.playlist import fetch_user_playlist
from utils.database import Base, Users, UserRecommendation, SpotifyData


class TestRecommendation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')  # Use in-memory database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
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
            self.session.add(UserRecommendation(user_id="user_id_1", song_id=song_id, rank=i))
            self.session.add(SpotifyData(song_id=song_id, song_name=f'Song {i}', artist_name=f'Singer {i}'))

        self.session.commit()

    def tearDown(self):
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_fetch_user_playlist_length(self):
        # Call fetch_user_playlist with a mocked session
        songs_list, artists_list, _ = fetch_user_playlist('user_id_1', session=self.session)
        # Assertions
        self.assertEqual(len(songs_list), 10)
        self.assertEqual(len(artists_list), 10)
        self.assertEqual(len(songs_list), len(artists_list))

    def test_nonexistent_user(self):
        # Test behavior for a non-existent user
        songs_list, artists_list, _ = fetch_user_playlist('user_id_nonexistent', session=self.session)
        self.assertEqual(songs_list, [])
        self.assertEqual(artists_list, [])

    def test_data_integrity(self):
        # Check if the fetched data matches the expected results
        songs_list, artists_list, _ = fetch_user_playlist('user_id_1', session=self.session)
        expected_songs = ['Song 1', 'Song 2', 'Song 3', 'Song 4', 'Song 5',
                          'Song 6', 'Song 7', 'Song 8', 'Song 9', 'Song 10']
        expected_artists = ['Singer 1', 'Singer 2', 'Singer 3', 'Singer 4', 'Singer 5',
                            'Singer 6', 'Singer 7', 'Singer 8', 'Singer 9', 'Singer 10']
        # No artist data in the test setup, so artists_list is expected to be empty
        self.assertEqual(songs_list, expected_songs)
        self.assertEqual(artists_list, expected_artists)


if __name__ == '__main__':
    unittest.main()