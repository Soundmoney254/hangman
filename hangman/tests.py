from django.test import TestCase, Client
from .models import Game

class HangmanTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_create_game(self):
        response = self.client.post('/game/new/')
        self.assertEqual(response.status_code, 201)
        self.assertTrue('id' in response.json())

    def test_show_game(self):
        game = Game()
        game.save()
        response = self.client.get(f'/game/{game.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('state' in response.json())
        self.assertTrue('word' in response.json())
        self.assertTrue('incorrect_guesses' in response.json())
        self.assertTrue('remaining_guesses' in response.json())

    def test_guess(self):
        game = Game()
        game.save()
        response = self.client.post(f'/game/{game.id}/guess/', {'guess': 'A'}, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('state' in response.json())
        self.assertTrue('word' in response.json())
        self.assertTrue('incorrect_guesses' in response.json())
        self.assertTrue('remaining_guesses' in response.json())
        self.assertTrue('correct_guess' in response.json())