from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    # TODO -- write tests for every view function / feature!
    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_show_home(self):
        """Make sure information is in the session and that the HTML is displayed"""
        with self.client:
            resp = self.client.get('/')
            self.assertIn('board', session)
            self.assertIn(b'Highscore:', resp.data)
            self.assertIn(b'Score:', resp.data)
            self.assertIn(b'Time:', resp.data)
            self.assertIsNone(session.get('nplays'))
    
    def test_word_validity(self):
        boggle = Boggle()
        board = [['D'],['O'],['G'],
                ['O'],['D'],['O'],
                ['C'],['J'],['K']]
        word = 'DOG'
        
        self.assertTrue(boggle.check_valid_word, (board, word))

