import unittest
from rocket_chat.rocket_chat import RocketChat
import os
from os.path import join, dirname
from dotenv import load_dotenv
import urllib


class TestRocketChat(unittest.TestCase):
    def setUp(self):
        load_dotenv(verbose=True)
        dotenv_path = join(dirname(__file__), '.env')
        load_dotenv(dotenv_path)
        self.aurhorized_user = os.environ.get("ROCKET_CHAT_USER")
        self.aurhorized_password = os.environ.get("ROCKET_CHAT_PASSWORD")
        self.rocket_chat_url = os.environ.get("ROCKET_CHAT_URL")

    def test_login_success(self):
        rocket_chat = RocketChat(self.rocket_chat_url, self.aurhorized_user, self.aurhorized_password)
        self.assertNotEqual(len(rocket_chat.auth_token), 0)
        self.assertNotEqual(len(rocket_chat.user_id), 0)

    def test_login_failed(self):
        with self.assertRaises(urllib.error.HTTPError):
            unauthorized_user = 'mbvdr678ijhvbjiutrdvbhjutrdfyuijhgf'
            unauthorized_pass = 'gfr67865tghjgfr567uijhfrt67ujhgthhh'
            RocketChat(self.rocket_chat_url, unauthorized_user, unauthorized_pass)


if __name__ == '__main__':
    unittest.main()