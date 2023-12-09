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
        self.session.begin_nested()  # Start a new transaction
        self.add_test_data()

    def add_test_data(self):
        valid_user = Users(
            user_id="user_id_1",
            first_name="Honorable",
            last_name="User",
        )
        self.session.add(valid_user)

        user_playlist_song1 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_1",
            rank=1
        )
        self.session.add(user_playlist_song1)

        user_playlist_song2 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_2",
            rank=2
        )
        self.session.add(user_playlist_song2)

        user_playlist_song3 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_3",
            rank=3
        )
        self.session.add(user_playlist_song3)

        user_playlist_song4 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_4",
            rank=4
        )
        self.session.add(user_playlist_song4)

        user_playlist_song5 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_5",
            rank=5
        )
        self.session.add(user_playlist_song5)

        user_playlist_song6 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_6",
            rank=6
        )
        self.session.add(user_playlist_song6)

        user_playlist_song7 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_7",
            rank=7
        )
        self.session.add(user_playlist_song7)

        user_playlist_song8 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_8",
            rank=8
        )
        self.session.add(user_playlist_song8)

        user_playlist_song9 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_9",
            rank=9
        )
        self.session.add(user_playlist_song9)

        user_playlist_song10 = UserRecommendation(
            user_id="user_id_1",
            song_id="song_id_10",
            rank=10
        )
        self.session.add(user_playlist_song10)

        valid_song1 = SpotifyData(
            song_id='song_id_1',
            song_name='Long Live',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song1)

        valid_song2 = SpotifyData(
            song_id='song_id_2',
            song_name='This Love',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song2)

        valid_song3 = SpotifyData(
            song_id='song_id_3',
            song_name='Haunted',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song3)

        valid_song4 = SpotifyData(
            song_id='song_id_4',
            song_name='Sparks Fly',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song4)

        valid_song5 = SpotifyData(
            song_id='song_id_5',
            song_name='Blank Space',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song5)

        valid_song6 = SpotifyData(
            song_id='song_id_6',
            song_name='Ours',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song6)

        valid_song7 = SpotifyData(
            song_id='song_id_7',
            song_name='Last Kiss',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song7)

        valid_song8 = SpotifyData(
            song_id='song_id_8',
            song_name='Cardigan',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song8)

        valid_song9 = SpotifyData(
            song_id='song_id_9',
            song_name='Karma',
            artist_name='Taylor Swift',
        )
        self.session.add(valid_song9)

        valid_song10 = SpotifyData(
            song_id='song_id_10',
            song_name='Red',
            artist_name='Taylor Swift'
        )
        self.session.add(valid_song10)

        self.session.commit()

    def tearDown(self):
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_fetch_user_playlist_length(self):
        # Call fetch_user_playlist with a mocked session
        songs_list, artists_list = fetch_user_playlist('user_id_1', session=self.session)

        # Assertions
        self.assertEqual(len(songs_list), 10)
        self.assertEqual(len(artists_list), 10)
        self.assertEqual(len(songs_list), len(artists_list))

    def test_nonexistent_user(self):
        # Test behavior for a non-existent user
        songs_list, artists_list = fetch_user_playlist('user_id_nonexistent', session=self.session)
        self.assertEqual(songs_list, [])
        self.assertEqual(artists_list, [])

    def test_data_integrity(self):
        # Check if the fetched data matches the expected results
        songs_list, artists_list = fetch_user_playlist('user_id_1', session=self.session)
        expected_songs = ['Long Live', 'This Love', 'Haunted', 'Sparks Fly', 'Blank Space',
                          'Ours', 'Last Kiss', 'Cardigan', 'Karma', 'Red']
        expected_artists = ['Taylor Swift', 'Taylor Swift', 'Taylor Swift', 'Taylor Swift', 'Taylor Swift',
                            'Taylor Swift', 'Taylor Swift', 'Taylor Swift', 'Taylor Swift', 'Taylor Swift']
        # No artist data in the test setup, so artists_list is expected to be empty
        self.assertEqual(songs_list, expected_songs)
        self.assertEqual(artists_list, expected_artists)


if __name__ == '__main__':
    unittest.main()