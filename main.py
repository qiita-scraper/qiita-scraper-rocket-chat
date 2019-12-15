import os

from rocket_chat import rocket_chat
from qiita import qiita

def main():
    url, user, password  = __get_os_environ()

    q = qiita.Qiita()
    rc = rocket_chat.RocketChat(url, user, password)

    for user in q.get_qiita_organization_users('intec'):
        articles = q.fetch_recent_user_articles(user)
        for yesterday_article in q.extract_yesterday_articles(articles):
            msg = rc.format_message(user=user, title=yesterday_article['title'], article_url=yesterday_article['url'])
            room_name = 'qiita'
            rc.send_message_to_rocket_chat(msg, room_name)


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


main()