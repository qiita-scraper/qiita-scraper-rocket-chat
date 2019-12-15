import datetime as dt
from bs4 import BeautifulSoup
from urllib import request
import time
import re

class Qiita:
    def __init__(self):
        pass

    def get_qiita_organization_users(self, organization_name):
        """
        Qiita Organizationに所属するユーザIDの一覧を取得する
        :param organization_name: Organization名 (example: intec)
        :return:
        """
        qiita_url = 'https://qiita.com/organizations/' + organization_name + '/members'
        users = []
        page = 0
        while True:
            page += 1
            response = request.urlopen(qiita_url + '?page=' + str(page))
            soup = BeautifulSoup(response, 'html.parser')
            response.close()
            members = soup.find_all('span', class_='od-MemberCardHeaderIdentities_userid')
            if len(members) == 0: break
            for m in members:
                user_id = m.string[1:]
                users.append(user_id)
        return users

    def fetch_recent_user_articles(self, user):
        """
        指定したユーザの投稿した Qiita 記事のうち、最新の記事を複数取得する
        :param user:
        :return:
        """

        qiita_url = 'https://qiita.com/' + user
        response = request.urlopen(qiita_url)
        soup = BeautifulSoup(response, 'html.parser')
        response.close()

        created_ats = []
        created_dates = soup.find_all('div', class_='ItemLink__info')
        for created_date in created_dates:
            div = re.sub('<a.*?>|</a>', '', str(created_date))
            text = re.sub('<div.*?>|</div>', '', div).split()
            month = str(time.strptime(text[3], '%b').tm_mon)
            day = text[4][:-1]
            year = text[5]
            created_at = year + '/' + month + '/' + day
            created_ats.append(created_at)

        articles = []
        a_tags = soup.find_all('a', class_='u-link-no-underline')
        for index, a in enumerate(a_tags):
            href = a.get('href')
            url = 'https://qiita.com' + href
            title = a.string
            articles.append({'title': title, 'url': url, 'created_at': created_ats[index]})

        return articles

    def extract_yesterday_articles(self, articles):
        """
        昨日投稿された記事を抽出する
        :param articles:
        :return:
        """
        yesterday = dt.date.today() - dt.timedelta(days=1)
        return [
            {'title': item.get('title'), 'url': item.get('url')} for item in articles
            if dt.datetime.strptime(item.get('created_at'), '%Y/%m/%d').date() == yesterday
        ]