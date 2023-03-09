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
    article_titles = []

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
                                        page_size=100,
                                        page=1)
    
    #Gets a list of all of the titles from the response
    titles = [article['title'] for article in response['articles']]
    #makes a blank title dictionary
    title_list = {}
    #makes a dictionary where each article has a unquie value we can put into the GPT prompt (being index+1)
    #the idea is to use this in a prompt like "Classify the articless in this dictionary has one of the following subjects:...
    #return a dictionary that is the articles' number and it's classification

    #! we need to eliminate similar articles before we sort this to eliminate tokens
    for index, title in enumerate(titles):
        title_list.update({index+1:title})

    return title_list

#prints results
result = test()
print(result)