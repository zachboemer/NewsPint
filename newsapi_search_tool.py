import os
import psycopg2
import pytz
import csv
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
    articles_to_add = []

    # timezone
    central = pytz.timezone('US/Central')

    # to param
    today = datetime.today()
    targetTime = time(hour=17)
    todayDatetime = datetime.combine(today, targetTime)
    formattedTodayDatetime = todayDatetime.isoformat()

    # from param
    yesterdayDatetime = todayDatetime - timedelta(days=1)
    formattedYesterdayDatetime = yesterdayDatetime.isoformat()

    #does the actual request to news API
    response = newsapi.get_everything(q='epsports',
                                        sources='',
                                        domains='',
                                        from_param=formattedYesterdayDatetime,
                                        to=formattedTodayDatetime,
                                        language='en',
                                        sort_by='popularity',
                                        page_size=30,
                                        page=1)
    
    return response

#prints results
result = test()
print(result)