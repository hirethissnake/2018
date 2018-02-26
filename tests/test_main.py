"""
Test game starting, responses, and validity of responses.
"""
import unittest
import json
import requests

class TestMain(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    URL = 'http://localhost:8080'

    def setUp(self):
        """
        Preempt each test with this.
        """
        self.check_server_status()

    def check_server_status(self):
        """
        Only run tests if we can connect to the bottle server at URL.
        """
        try:
            requests.get(str(self.URL))
        except requests.ConnectionError:
            print('Was not able to connect to server. Confirm server is running at {}'.format(self.URL))
            self.skipTest(TestMain)

    def test_start_response(self):
        """
        Test required responses to '/start' POST
        """
        paramData = {
            'width': 20,
            'height': 20,
            'game_id': 'game1'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(str(self.URL) + '/start', json=paramData, headers=headers)
        responseData = json.loads(r.text)

        self.assertIn('color', responseData)
        self.assertIn('head_url', responseData)
        self.assertIn('name', responseData)
        self.assertIn('taunt', responseData)

    def test_optional_start_responses(self):
        """
        Test optional responses to '/start' POST
        """
        paramData = {
            'width': 20,
            'height': 20,
            'game_id': 'game1'
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(str(self.URL) + '/start', json=paramData, headers=headers)
        responseData = json.loads(r.text)

        self.assertIn('head_type', responseData)
        self.assertIn('tail_type', responseData)
        # self.assertIn('secondary_color', responseData)

    def test_move_responses(self):
        """
        Test required responses to '/move' POST
        """
        paramData = {
            "snakes": [
                {
                    "taunt": "git gud",
                    "name": "my-snake",
                    "id": "25229082-f0d7-4315-8c52-6b0ff23fb1fb",
                    "health_points": 93,
                    "coords": [[0, 0], [0, 1], [0, 2]]},
                {
                    "taunt":
                    "cash me outside",
                    "name": "angry-whitegirl",
                    "id": "ex-uuid",
                    "health_points": 93,
                    "coords": [[15, 14], [15, 13], [15, 12]]}
            ],
            "width":20,
            "height":20,
            "game_id": "game1",
            "food": [[4, 5], [8, 9]],
            "you": "25229082-f0d7-4315-8c52-6b0ff23fb1fb"
        }
        headers = {
            'Content-Type': 'application/json'
        }
        r = requests.post(str(self.URL) + '/move', json=paramData, headers=headers)
        responseData = json.loads(r.text)

        self.assertIn('move', responseData)
        self.assertIn('taunt', responseData)

        self.assertIn(responseData['move'], ['up', 'right', 'down', 'left'])
