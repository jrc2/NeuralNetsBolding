import tweepy as tp
import numpy as np
import csv
import time
import re
from datetime import datetime, timedelta
import connections as conn

conn

auth = tp.OAuthHandler(conn.consumer_key, conn.consumer_secret)
auth.set_access_token(conn.access_token, conn.access_token_secret)
auth_api = tp.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

account_list = ['JoeBiden', 'realDonaldTrump', 'espn', 'JoelOsteen', 'HuaweiUK', 'Google', 
                'NPR', 'brave']

found_tweets = []


def upload_tweets():
  if len(found_tweets) == 0:
    print("No tweets to upload")
  else:
    print("adding tweets to DB")
    cursor = conn.db.cursor()
    query = "INSERT INTO tweets(username, content, category) VALUES(%s, %s, %s)"
    cursor.executemany(query, found_tweets)
    conn.db.commit()
    cursor.close()
    found_tweets.clear()
    
    
def save_tweets():
  with open('test2.csv', 'a+') as f:
    print('writing tweets to csv')
    csv.writer(f).writerows(found_tweets)
    found_tweets.clear()
  
num_tweets = 0 
if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    tweets = item.statuses_count
    hashtags = []
    mentions = []
    end_date = datetime.utcnow() - timedelta(days=365)
    for tweet in tp.Cursor(auth_api.user_timeline, id=target).items():
      if (num_tweets + 1) % 150 == 0:
        #upload_tweets()
        save_tweets()
      status = auth_api.get_status(tweet.id, tweet_mode="extended")
      if not hasattr(status, "retweeted_status"):  # Don't include retweets
        content = re.sub(
          "(https://t.co/)[\S]+|[^\w\d\s!$%&*\(\)\-_=\+,./?:;\"']", 
          '', 
          status.full_text)
        if len(content) >= 60:
          found_tweets.append((target, content.encode("utf-8"), "test"))
          num_tweets += 1
      if status.created_at < end_date:
        break
        
#upload_tweets()
save_tweets()
