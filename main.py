import os

from rocket_chat import rocket_chat
from qiita import qiita
import yaml


def main():
    url, user, password  = __get_os_environ()
    room_name, organization = __get_config()

    q = qiita.Qiita()
    rc = rocket_chat.RocketChat(url, user, password)

    for user in q.fetch_organization_users(organization):
        articles = q.fetch_recent_user_articles(user)
        for yesterday_article in q.extract_yesterday_articles(articles):
            msg = rc.format_message(user=user, title=yesterday_article['title'], article_url=yesterday_article['url'])
            rc.send_message_to_rocket_chat(msg, room_name)


def __get_config():
    f = open("config.yml", "r")
    data = yaml.load(f)
    room_name = data.get('rocket_chat').get('room_name')
    organization = data.get('qiita').get('organization')
    return room_name, organization


def __get_os_environ():
    url = os.environ.get('ROCKET_CHAT_URL')
    user = os.environ.get('ROCKET_CHAT_USER')
    password = os.environ.get('ROCKET_CHAT_PASSWORD')
    if url is None or len(url) == 0:
        raise Exception('ROCKET_CHAT_URL is not set in environment variable')
    if user is None or len(user) == 0:
        raise Exception('ROCKET_CHAT_USER is not set in environment variable')
    if password is None or len(password) == 0:
        raise Exception('ROCKET_CHAT_PASSWORD is not set in environment variable')
    return url, user, password


def handler(event, context):
    main()
