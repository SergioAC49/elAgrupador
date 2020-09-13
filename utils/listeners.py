import tweepy, re, json, traceback
from utils.newspapers import *
from utils.scrapers import *
from utils.elasticsearch_connector import save_news, print_all_news

import time, logging

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')

#Coloca dentro de las comillas tus claves...
CONSUMER_KEY = 'ppEPCYun4gVJAQp8ZbLfmolHK' 
CONSUMER_SECRET = 'ZIT65OtGaWpSGO0PiSMs7Y9rnypqFC7DGiWdkhGBBISFx8BwIM'
ACCESS_KEY = '485960475-oxS67aDdUpd3NpDbEMREmJXowMGxumd5m9fF5A8X'
ACCESS_SECRET = 'MGVcjIcObqdsFefNaVBXGhFVjTLzha7ljTT8WrCQYpNF7'

#En esta parte nos identifica para poder realizar operaciones
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

api = tweepy.API(auth)


def get_scraper(newspaper, url):
    Scraper = newspapers.get(newspaper)["scrapper"]
    return Scraper(url)

# Override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):

    def __init__(self, newspaper):
        # Invoke StreamListener constructor
        tweepy.StreamListener.__init__(self)
        # New attributes
        self.newspaper = newspaper

    def on_status(self, status):
        logging.info("==========================================")
        # Test if the tweet is from the newspaper account
        # Discard RT and mentions from other users
        newspaper = self.newspaper
        if status.user.id == int(newspapers.get(newspaper)["twitterID"]):
            tweetDict = status._json
            logging.info(f'Newspaper: {newspapers.get(newspaper)["name"]}')
            logging.info(f'Tweet: {tweetDict.get("text")}')
            try:
                if tweetDict.get("entities").get("urls"):
                    url = tweetDict.get("entities").get("urls")[0].get("expanded_url")
                    logging.info(url)
                    if newspapers.get(newspaper)["baseURL"] in url: 
                        scraper = get_scraper(newspaper, url)
                        res = save_news(scraper)
                        logging.info(res)
                    else:
                        logging.info("The url is not from the newspaper webpage")
                else: 
                    logging.info("There is not an URL in the tweet") 
            except Exception as e:
                logging.info("An exception occurred:") 
                logging.info(e)



    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

    def my_start(self):
        myStream = tweepy.Stream(auth = api.auth, listener=self)
        myStream.filter(follow=[newspapers.get(self.newspaper)["twitterID"]], is_async=True)
