from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import sqlite3  
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time

analyzer = SentimentIntensityAnalyzer()

conn = sqlite3.connect('twitter.db')
c = conn.cursor()

def create_table():
    try:
        c.execute("CREATE TABLE IF NOT EXISTS sentiment(unix REAL, tweet TEXT, sentiment REAL)")
        c.execute("CREATE INDEX fast_unix ON sentiment(unix)")
        c.execute("CREATE INDEX fast_tweet ON sentiment(tweet)")
        c.execute("CREATE INDEX fast_sentiment ON sentiment(sentiment)")
        conn.commit()
    except Exception as e:
        print(str(e))
create_table()

#consumer key, consumer secret, access token, access secret.-
ckey="jAHcFMwsHnlXFn7QoeOFnrDVM"
csecret="vso04wiUmmw39yfqyCTfsj0njLESXw6RJZchuGIm4CDj6qfIto"
atoken="1670410170-F1Ve5jLNYWjSzncxCOGig1a97Ze3UaY6BcBhID1"
asecret="qDqGBMyJMFJKq2tMZngnOEoLibs2ICLdjHc4Kk9eTGBA2"

class listener(StreamListener):

    def on_data(self, data):
        try:
            data = json.loads(data)
            tweet = unidecode(data['text'])
            time_ms = data['timestamp_ms']
            vs = analyzer.polarity_scores(tweet)
            sentiment = vs['compound']
            print(time_ms, tweet, sentiment)
            c.execute("INSERT INTO sentiment (unix, tweet, sentiment) VALUES (?, ?, ?)",
                  (time_ms, tweet, sentiment))
            conn.commit()

        except KeyError as e:
            print(str(e))
        return(True)

    def on_error(self, status):
        print(status)

while True:

    try:
        auth = OAuthHandler(ckey, csecret)
        auth.set_access_token(atoken, asecret)
        twitterStream = Stream(auth, listener())
        twitterStream.filter(track=["Duterte", "Bong Go", "Hilbay", "Pilo Hilbay", "duterte", "a"])
    except Exception as e:
        print(str(e))
        time.sleep(5)