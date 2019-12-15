import json
from urllib import request, parse, error


class RocketChat:
    def __init__(self, url, user, password):
        self.url = url
        self.auth_token, self.user_id = self.__login_rocket_chat(user, password)

    def __login_rocket_chat(self, user, password):
        """
        Rocket Chatにログインして auth_token と user_id を取得します。
        :param url:
        :return:
        """
        obj = {
            "user": user,
            "password": password
        }
        json_data = json.dumps(obj).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        req_object = request.Request(self.url + '/api/v1/login', data=json_data, headers=headers, method='POST')
        with request.urlopen(req_object) as response:
            response_body = response.read().decode("utf-8")
            result_objs = json.loads(response_body.split('\n')[0])
            user_id = result_objs["data"]["userId"]
            auth_token = result_objs["data"]["authToken"]
            print(user_id, auth_token)
        return auth_token, user_id

    def send_message_to_rocket_chat(self, msg, room_name):
        """
        Rocket Chatにメッセージを送信する
        :param msg:
        :param room_name
        :return:
        """
        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.auth_token,
            "X-User-Id": self.user_id
        }
        print(headers)
        body = {
            "message": {
                "rid": self.fetch_room_id(room_name),
                "msg": msg,
                "alias": 'Qiita Bot',
                "avatar": 'https://haskell.jp/antenna/image/logo/qiita.png'
            }
        }
        print(body)
        req_object = request.Request(self.url + '/api/v1/chat.sendMessage', data=json.dumps(body).encode("utf-8"), headers=headers, method="POST")
        with request.urlopen(req_object) as response:
            response_body = response.read().decode("utf-8")
            print(response_body)

    def fetch_room_id(self, room_name):
        """
        Rocket Chat の room_id を取得します。
        :param room_name:
        :return:
        """

        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.auth_token,
            "X-User-Id": self.user_id
        }
        params = {'roomName': room_name}
        url = '{}?{}'.format(self.url + '/api/v1/channels.info', parse.urlencode(params))
        req_object = request.Request(url, headers=headers, method="GET")
        try:
            with request.urlopen(req_object) as response:
                response_body = response.read().decode("utf-8")
                print(response_body)
                result_objs = json.loads(response_body.split('\n')[0])
                channel = result_objs.get('channel')
                return channel.get('_id')
        except error.HTTPError as err:
            print('/api/v1/channels.info ', err.code)
            return self.fetch_private_room_id(room_name)
        except error.URLError as err:
            print('/api/v1/channels.info ', err.reason)
            return self.fetch_private_room_id(room_name)

    def fetch_private_room_id(self, room_name):
        """
        Rocket Chat の プライベート room_id を取得します。
        :param room_name:
        :return:
        """

        headers = {
            "Content-Type": "application/json",
            "X-Auth-Token": self.auth_token,
            "X-User-Id": self.user_id
        }
        params = {'roomName': room_name}
        url = '{}?{}'.format(self.url + '/api/v1/groups.info', parse.urlencode(params))
        req_object = request.Request(url, headers=headers, method="GET")
        try:
            with request.urlopen(req_object) as response:
                response_body = response.read().decode("utf-8")
                print(response_body)
                result_objs = json.loads(response_body.split('\n')[0])
                channel = result_objs.get('group')
                room_id = channel.get('_id')
        except error.HTTPError as err:
            print(err.code)
        except error.URLError as err:
            print('/api/v1/groups.info ', err.reason)
        return room_id

    def format_message(self, user, title, article_url):
        """
        送信するメッセージを加工します。
        :param user:
        :param title:
        :param article_url:
        :return:
        """

        base_txt = '''{user} さんが Qiita に記事を投稿しました 🎉
    
        {title}
        {article_url}
        '''
        return base_txt.format(user=user, title=title, article_url=article_url)
