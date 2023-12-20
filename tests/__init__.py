"""
Initializes the test suite of Spotify Music Exploration/Recommendation System.

It imports the tests modules for various components of the system, including
database, visualization, login, and recommendation.
"""

# Import test modules for different components
from . import test_database, test_visual, test_login, test_recom

# Specify modules available when importing the package
__all__ = ["test_database", "test_visual", "test_login", "test_recom"]
