# qiita-scraper-rocket-chat

`qiita-scraper-rocket-chat` is a bot that notifies RocketChat of new posts from users who belong to Qiita Organization.

Set the connection information in config.yml.

```
rocket_chat:
  room_name: <<your rocket chat room name to post>>

qiita:
  organization: <<your qiita organization name>>
```

To run this bot on AWS Lambda, use the serverless framework. Execute the following command to deploy.

```
$ npm install
```

```
$ sls deploy --url <<your_rocket_chat_endpoint>> --user <<login_user>> --password <<login_password>>
```

# Development

```
$ git clone https://github.com/qiita-scraper/qiita-scraper-rocket-chat.git
$ cd qiita-scraper-rocket-chat
$ python3 -v venv .venv
$ . .venv/bin/activate
(.venv) $ pip install -r requirements.txt
(.venv) $ pip install -r requirements-dev.txt
(.venv) $ <<Ready for development>>
```

# Test

```
export ROCKET_CHAT_USER=<<your rocket chat user email>>
export ROCKET_CHAT_PASSWORD=<<your rocket chat user password>>
export ROCKET_CHAT_URL=<< your rocket chat url>>
```

```
$ python -m unittest test.py
```
