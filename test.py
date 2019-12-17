import unittest
from rocket_chat.rocket_chat import RocketChat
import urllib
from qiita.qiita import Qiita
import freezegun
import json

class TestQiitaScraper(unittest.TestCase):
    def setUp(self):
        # rocket chat admin user set in docker-compoose.yml rocketchat service environment value.
        self.aurhorized_user = 'admin'
        self.aurhorized_password = 'supersecret'
        self.rocket_chat_url = 'http://localhost:3000'

    def test_login_success(self):
        rocket_chat = RocketChat(self.rocket_chat_url, self.aurhorized_user, self.aurhorized_password)
        self.assertNotEqual(len(rocket_chat.auth_token), 0)
        self.assertNotEqual(len(rocket_chat.user_id), 0)

    def test_login_failed(self):
        with self.assertRaises(urllib.error.HTTPError):
            unauthorized_user = 'mbvdr678ijhvbjiutrdvbhjutrdfyuijhgf'
            unauthorized_pass = 'gfr67865tghjgfr567uijhfrt67ujhgthhh'
            RocketChat(self.rocket_chat_url, unauthorized_user, unauthorized_pass)

    def test_fetch_organization_users_success(self):
        q = Qiita()
        self.assertTrue(len(q.fetch_organization_users('intec')) > 0)

    def test_fetch_organization_users_failed(self):
        q = Qiita()
        with self.assertRaises(urllib.error.HTTPError):
            q.fetch_organization_users('xxxxxxxxx_unknown_organization')


    def test_fetch_recent_user_articles_success(self):
        q = Qiita()
        self.assertTrue(len(q.fetch_recent_user_articles('G-awa')) > 0)

    def test_fetch_recent_user_articles_failed(self):
        q = Qiita()
        with self.assertRaises(urllib.error.HTTPError):
            q.fetch_recent_user_articles('xxxxxxxx_unknown_user')

    # freezegunを使用して現在時刻を置換
    @freezegun.freeze_time('2019-12-02 12:34:56')
    def test_extract_yesterday_article(self):
        q = Qiita()
        user_articles =[{'title': 'サーバレスフレームワークに触れる', 'url': 'https://qiita.com/aj2727/items/155f1df552425c4b7bc6',
          'created_at': '2019/12/15'},
         {'title': 'サーバーレスに触れる', 'url': 'https://qiita.com/aj2727/items/f95ec1902034bd97d836',
          'created_at': '2019/12/07'},
         {'title': 'motoを初めて使うまでの道のり', 'url': 'https://qiita.com/aj2727/items/ae64617839c2ed2217d7',
          'created_at': '2019/12/01'}]
        self.assertTrue(len(q.extract_yesterday_articles(user_articles)) == 1)

    # freezegunを使用して現在時刻を置換
    @freezegun.freeze_time('2019-12-01 12:34:56')
    def test_dont_extract_yesterday_article(self):
        q = Qiita()
        user_articles =[{'title': 'サーバレスフレームワークに触れる', 'url': 'https://qiita.com/aj2727/items/155f1df552425c4b7bc6',
          'created_at': '2019/12/17'},
         {'title': 'サーバーレスに触れる', 'url': 'https://qiita.com/aj2727/items/f95ec1902034bd97d836',
          'created_at': '2019/12/07'},
         {'title': 'motoを初めて使うまでの道のり', 'url': 'https://qiita.com/aj2727/items/ae64617839c2ed2217d7',
          'created_at': '2019/12/01'}]
        self.assertTrue(len(q.extract_yesterday_articles(user_articles)) == 0)

    # freezegunを使用して現在時刻を置換
    @freezegun.freeze_time('2019-12-07 12:34:56')
    def test_extract_yesterday_articles(self):
        q = Qiita()
        user_articles =[{'title': 'サーバレスフレームワークに触れる', 'url': 'https://qiita.com/aj2727/items/155f1df552425c4b7bc6',
          'created_at': '2019/12/06'},
         {'title': 'サーバーレスに触れる', 'url': 'https://qiita.com/aj2727/items/f95ec1902034bd97d836',
          'created_at': '2019/12/06'},
         {'title': 'motoを初めて使うまでの道のり', 'url': 'https://qiita.com/aj2727/items/ae64617839c2ed2217d7',
          'created_at': '2019/12/06'}]
        self.assertTrue(len(q.extract_yesterday_articles(user_articles)) == 3)

def suite():
  suite = unittest.TestSuite()
  suite.addTests(unittest.makeSuite(TestQiitaScraper))
  return suite

if __name__ == '__main__':
    unittest.main()