import tweepy as tp
from datetime import datetime, timedelta
import connections as conn

conn

auth = tp.OAuthHandler(conn.consumer_key, conn.consumer_secret)
auth.set_access_token(conn.access_token, conn.access_token_secret)
auth_api = tp.API(auth)

account_list = ['realDonaldTrump', 'JoeBiden']
  
if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    print("screen_name: " + item.screen_name)
    tweets = item.statuses_count
    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=10)
    for tweet in tp.Cursor(auth_api.user_timeline, id=target).items():
      status = auth_api.get_status(tweet.id, tweet_mode="extended")
      if hasattr(status, "retweeted_status"):  # Check if Retweet
        print("it's a retweet")
      else:
        try:
          print(status.full_text)
          print("\n\n\n\n\n\n\n\n")
        except AttributeError:
          print("error")
      if status.created_at < end_date:
        break