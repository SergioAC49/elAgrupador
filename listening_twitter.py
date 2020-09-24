import argparse

from utils.scrapers import *
from utils.listeners import *
from utils.newspapers import *
from utils.elasticsearch_connector import print_all_news

import time, logging

logging.basicConfig(level=logging.INFO, format='%(threadName)s: %(message)s')


if __name__ == '__main__':
    """
    Call the script as: 
    python3 listening_twitter.py --newspaper {newspaper}
    
    """
    # Read arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--newspaper", required=True, help="name of the newspaper")

    args = parser.parse_args()
    newspaper = args.newspaper.lower()

    listener = MyStreamListener(newspaper)
    listener.my_start()

    # Print all the news saved in elasticsearch (to check if we have saved them)
    #print_all_news()
