"""
Unit Testing for Visualizations in Spotify Music Exploration/Recommendation System.

This module contains tests for the visualizations presented on the Explore page
of the web application, ensuring accurate data representation and functionality.
It covers tests for retrieving data range, song attributes, and attribute trends.
"""

import unittest
from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.utils.pages.explore.visuals import get_min_max_years, update_song_attributes,\
                                         update_attribute_trend
from app.utils.database import Base, SpotifyData, DataByYear


class TestVisual(unittest.TestCase):
    """
    A TestCase class for testing visualizations on the Explore page.

    This class includes methods for setting up a test database environment,
    adding test data, and defining various test cases for visual functionalities.
    """
    @classmethod
    def setUpClass(cls):
        """
        Set up an in-memory SQLite database for testing visualization features.

        This method initializes a SQLite in-memory database and prepares
        table schemas for SpotifyData and DataByYear.
        """
        cls.engine = create_engine("sqlite:///:memory:")  # Use in-memory database for testing
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        """
        Prepare the database session and add test data before each test.

        This method initializes a new database session and adds test data
        for SpotifyData and DataByYear before each test case is run.
        """
        self.session = self.Session()
        self.add_test_data()

    def add_test_data(self):
        """
        Add test data for SpotifyData and DataByYear to the database.

        This method clears any existing records and inserts test data for
        visualizations, including SpotifyData samples and DataByYear records.
        """
        self.session.query(SpotifyData).delete()
        self.session.query(DataByYear).delete()

        # Add test data for SpotifyData and DataByYear
        spotify_data_sample = SpotifyData(
            song_id="7DjCRhhFo9PPzca1BjMLcf",
            song_name="Long Live",
            artist_id="349a6f757a",
            artist_name="Taylor Swift",
            year=2010,
            valence=0.142,
            acousticness=0.036,
            danceability=0.418,
            energy=0.68,
            instrumentalness=7.59e-05,
            liveness=0.114,
            speechiness=0.0347
        )
        self.session.add(spotify_data_sample)

        data_by_year_2000 = DataByYear(
            id=1,
            year=2000,
            valence=0.102,
            acousticness=0.076,
            danceability=0.218,
            energy=0.28,
            instrumentalness=1.59e-01,
            liveness=0.714,
            speechiness=0.47,
        )
        self.session.add(data_by_year_2000)

        data_by_year_2010 = DataByYear(
            id=2,
            year=2010,
            valence=0.142,
            acousticness=0.036,
            danceability=0.418,
            energy=0.68,
            instrumentalness=7.59e-05,
            liveness=0.114,
            speechiness=0.0347,
        )
        self.session.add(data_by_year_2010)

        data_by_year_2020 = DataByYear(
            id=3,
            year=2020,
            valence=0.52,
            acousticness=0.36,
            danceability=0.718,
            energy=0.98,
            instrumentalness=7.59e-02,
            liveness=0.14,
            speechiness=0.0947,
        )
        self.session.add(data_by_year_2020)

        self.session.commit()

    def tearDown(self):
        """
        Rollback the database transaction after each test.

        This method ensures database isolation between tests by rolling back
        any changes made during the test execution.
        """
        self.session.rollback()  # Rollback the transaction
        self.session.close()

    def test_get_min_max_years(self):
        """
        Test the retrieval of minimum and maximum years for visualization.

        This test ensures that get_min_max_years function correctly fetches
        the range of years from the DataByYear table for visualization purposes.
        """
        min_year, max_year = get_min_max_years(session=self.session)
        self.assertEqual(min_year, 2000)
        self.assertEqual(max_year, 2020)

    @patch("plotly.express.line_polar")
    def test_update_song_attributes(self, mock_px_line_polar):
        """
        Test the functionality of update_song_attributes function.

        This test checks if update_song_attributes correctly invokes the
        Plotly express line_polar function for a valid song.
        """
        # Test for a valid song
        update_song_attributes("Long Live", session=self.session)
        mock_px_line_polar.assert_called_once()

    def test_update_attribute_trend(self):
        """
        Test the attribute trend visualization based on the year range.

        This test checks the functionality of update_attribute_trend to ensure
        it generates the correct figures for valid and invalid year ranges.
        """
        # Test for a valid range and attributes
        fig = update_attribute_trend(
            ["acousticness", "danceability"],
            [2020, 2020],
            session=self.session
        )
        self.assertIsNotNone(fig)
        self.assertTrue(len(fig.data) > 0)

        # Test for an invalid range (where no data is present)
        empty_fig = update_attribute_trend(
            ["acousticness", "danceability"],
            [1900, 1900],
            session=self.session
        )
        self.assertIsNotNone(empty_fig)
        self.assertTrue(len(empty_fig.data) == 0)


if __name__ == "__main__":
    unittest.main()
