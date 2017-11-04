import json
import time
import praw
import feedparser
import html2text

import config
from funcs import chunks


# Create reddit client
reddit = praw.Reddit(
    client_id=config.reddit['client_id'],
    client_secret=config.reddit['client_secret'],
    user_agent=config.reddit['user_agent'],
    username=config.reddit['username'],
    password=config.reddit['password']
)
subreddit = reddit.subreddit(config.reddit['subreddit'])

# Get history
# History is just a basic dict saved to a json file.
# The key is the feed name and value is the unique title of the most recently posted entry
try:
    with open(config.historyfile) as data_file:
        history = json.load(data_file)
except IOError:
    history = {}

# Parse feeds
for name, url in config.feeds:
    # Check if we have history
    if name not in history:
        history[name] = ""

    # Check if we have a new entry to post
    feed = feedparser.parse(url)
    if feed['entries'][0]['title_unique'] != history[name]:
        # Check its not just a blank because it's a first run
        entry = feed['entries'][0]

        if history[name] != "":
            # Post the entry to reddit
            h = html2text.HTML2Text()
            h.ignore_images = True

            title = "[%s] %s" % (name, entry['title'])
            text = h.handle(entry['content'][0]['value'])
            text = "%s\n\n%s" % (entry['link'], text)
            text = chunks(text, 40000)

            submission = subreddit.submit(
                title,
                selftext=text[0],
                send_replies=config.reddit['send_replies']
            )
            print "Submitted: %s" % submission.title
            time.sleep(10)

            # Post the rest of the text in comments if needed
            content = text
            if len(content) > 0:
                # Switch to 10k char limit for comments
                content.reverse()
                content.pop()
                content.reverse()
                content = chunks("".join(text), 10000)
                content.reverse()

            while len(content) > 0:
                print "Replying with more text to %s" % submission
                submission = submission.reply(content.pop())
                time.sleep(10)

        history[name] = entry['title_unique']


# Write the history file back to disk
with open(config.historyfile, "w") as data_file:
    data_file.write(json.dumps(history))
