import os
import psycopg2

from dotenv import load_dotenv
from newsapi import NewsApiClient
from datetime import datetime, time, timedelta

# loads .env variables
load_dotenv()
# setting up connection to NewsAPI
api_key = os.environ['API_KEY']
newsapi = NewsApiClient(api_key=api_key)

# setting up connection to our DB
db_url = os.environ['DATABASE_URL']
conn = psycopg2.connect(db_url, sslmode='require')

# to param
today = datetime.today()
targetTime = time(hour=17)
todayDatetime = datetime.combine(today, targetTime)
formattedTodayDatetime = todayDatetime.isoformat()

# from param
yesterdayDatetime = todayDatetime - timedelta(days=1)
formattedYesterdayDatetime = yesterdayDatetime.isoformat()

# request for esports news
response = newsapi.get_everything(
    q='esports', from_param=formattedYesterdayDatetime, to=formattedTodayDatetime, language='en', sort_by='popularity')


for article in response['articles']:
    source_name = article['source']['name']
    title = article['title']
    author = article['author']
    publish_date = article['publishedAt']
    retrieval_date = formattedTodayDatetime
    url = article['url']
    image_url = article['urlToImage']
    summary = article['description']

    print(title)

    # this bit of code inserts a single article into the DB
    # we will need to do checks above to devide which articles we will be adding, and only run thsi code if it passes
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO articles (source_name, title, author, publish_date, retrieval_date, url, image_url, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",

            (source_name, title, author, publish_date,
             retrieval_date, url, image_url, summary)
        )
conn.commit()  # this line actually sends the commands to the DB to execute
conn.close()  # closes connection so that we dont have any leaks
