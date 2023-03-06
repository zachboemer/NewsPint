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

    #imports the search domains from the csv file
    with open('approved_domains.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        search_domains = [domain for sublist in csv_reader for domain in sublist]
    search_domains_str = ",".join(search_domains)

    #does the actual request to news API
    response = newsapi.get_everything(q='us',
                                        sources='',
                                        domains=search_domains_str,
                                        from_param=formattedYesterdayDatetime,
                                        to=formattedTodayDatetime,
                                        language='en',
                                        sort_by='popularity',
                                        page_size=10,
                                        page=1)
    
    return response

#prints results
result = test()
print(result)