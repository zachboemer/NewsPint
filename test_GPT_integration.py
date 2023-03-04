import os
import psycopg2
import pytz
from dotenv import load_dotenv
from newsapi import NewsApiClient
from datetime import datetime, time, timedelta

def test():

    # loads .env variables
    load_dotenv()
    # setting up connection to NewsAPI
    api_key = os.environ['NEWS_API_KEY']
    newsapi = NewsApiClient(api_key=api_key)

    #create blank array
    all_articles = []

    # timezone
    central = pytz.timezone('US/Central')

    all_articles = newsapi.get_everything(q='',
                                        sources='',
                                        domains='',
                                        from_param='2023-03-02',
                                        to='2023-03-03',
                                        language='en',
                                        sort_by='relevancy',
                                        page=2)
    
    return all_articles

result = test()
print(result)