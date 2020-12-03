import tweepy
import csv
import re
from datetime import datetime, timedelta
import connections


###############################################
# Controls interactions with the Twitter API. #
# Make sure you have Twitter API credentials  #
# saved in connections.py                     #
###############################################

    
def write_tweets_to_csv(file_name, found_tweets):
    with open(file_name, 'a+') as f:
        print('Writing Tweets to CSV...')
        csv.writer(f).writerows(found_tweets)
        print("Tweets written to CSV!\n")


def save_tweets(usernames_list, num_days, file_name, min_length=60):
    found_tweets = []
    num_tweets = 0 

    if len(usernames_list) > 0:
        for target in usernames_list:
            print("Getting data for " + target)
            end_date = datetime.utcnow() - timedelta(days=num_days)
            for tweet in tweepy.Cursor(twitter_api.user_timeline, id=target).items():
                if (num_tweets + 1) % 150 == 0:
                    write_tweets_to_csv(file_name, found_tweets)
                    found_tweets.clear()
                status = twitter_api.get_status(tweet.id, tweet_mode="extended")
                if not hasattr(status, "retweeted_status"):  # Don't include retweets
                    content = re.sub(
                        "(https://t.co/)[\S]+|[^\w\d\s!$%&*\(\)\-_=\+,./?:;\"']", 
                        '', 
                        status.full_text)
                    if len(content) >= min_length:
                        found_tweets.append((target, content.encode("utf-8")))
                        num_tweets += 1
                if status.created_at < end_date:
                    break

    write_tweets_to_csv(file_name, found_tweets)
    print(f"All requested Tweets have been written to {file_name}\n")


def post_tweet(content):
    twitter_api.update_status(status=content)


twitter_auth = tweepy.OAuthHandler(connections.consumer_key, connections.consumer_secret)
twitter_auth.set_access_token(connections.access_token, connections.access_token_secret)
twitter_api = tweepy.API(twitter_auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)