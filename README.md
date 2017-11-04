# Reddit RSS Bot

Dead simple script to submit new RSS feed submissions to a subreddit.

## Installation
```
mkdir reddit-rss-bot
cd reddit-rss-bot
virtualenv .
source bin/activate
git clone https://github.com/skyride/reddit-rss-bot.git
cd reddit-rss-bot
cp config.py.example config.py
```

Fill out config.py with your info, then stick checknews.py in your crontab.
