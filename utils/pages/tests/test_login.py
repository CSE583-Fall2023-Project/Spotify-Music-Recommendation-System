"""Test the log-in system"""
import unittest
from sqlalchemy.orm import sessionmaker

from utils.pages.login import usermatch
from utils.database import Users, engine

Session = sessionmaker(bind=engine)
session = Session()


class TestLogin(unittest.TestCase):

    def test_login_smoke(self):
        assert (True)  # do something useful here
