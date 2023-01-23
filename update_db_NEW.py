import os
import psycopg2

from dotenv import load_dotenv
from newsapi import NewsApiClient
from datetime import datetime, time, timedelta


def main():

    # loads .env variables
    load_dotenv()
    # setting up connection to NewsAPI
    api_key = os.environ['NEWS_API_KEY']
    newsapi = NewsApiClient(api_key=api_key)

    # setting up connection to our DB
    db_url = os.environ['DATABASE_URL']
    conn = psycopg2.connect(db_url, sslmode='require')

    # declare empty arrays
    articlesToAdd = []
    domains = []

    # no science category because the articles are low quality
    categories = ['technology', 'business',
                  'entertainment', 'sports', 'health']
    queries = ['esports', 'politics', 'city planning']

    # to param
    today = datetime.today()
    targetTime = time(hour=17)
    todayDatetime = datetime.combine(today, targetTime)
    formattedTodayDatetime = todayDatetime.isoformat()

    # from param
    yesterdayDatetime = todayDatetime - timedelta(days=1)
    formattedYesterdayDatetime = yesterdayDatetime.isoformat()
    # gets comma seperated list of sources of each category
    for category in categories:
        domains.append(sourceListToString(newsapi.get_sources(category=category,
                                                              language='en')))
    for categoryDomains in domains:
        numOfArticlesAddedOfCategory = 0
        response = newsapi.get_everything(
            domains=categoryDomains,
            exclude_domains='',
            from_param=formattedYesterdayDatetime,
            to=formattedTodayDatetime,
            language='en',
            sort_by='popularity',
            page_size=10
        )
        # just adds the first two articles in the response
        for article in response['articles']:
            if numOfArticlesAddedOfCategory == 2:
                break
            # code for only allowing 1 of each source - we werent't getting a lot of articles in response so commented this out for now
            # sourceAlreadyAdded = False
            # for filteredArticle in articlesToAdd:
            #     if (article['source']['name'] == filteredArticle['source']['name']):
            #         sourceAlreadyAdded = True
            #         break
            # if sourceAlreadyAdded:
            #     continue
            articlesToAdd.append(article)
            numOfArticlesAddedOfCategory += 1

    for query in queries:
        response = newsapi.get_everything(
            q=query,
            exclude_domains='',
            from_param=formattedYesterdayDatetime,
            to=formattedTodayDatetime,
            language='en',
            sort_by='popularity',
            page_size=10)
        numOfArticlesAdded = 0
        for article in response['articles']:
            if numOfArticlesAdded == 2:
                break
            articlesToAdd.append(article)
            numOfArticlesAdded += 1
    # traverse through articlesToAdd, and then insert one by one into articles table
    for article in articlesToAdd:
        source_name = article['source']['name']
        title = article['title']
        author = article['author']
        publish_date = article['publishedAt']
        retrieval_date = formattedTodayDatetime
        url = article['url']
        image_url = article['urlToImage']
        summary = article['description']

        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO articles (source_name, title, author, publish_date, retrieval_date, url, image_url, summary) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",

                (source_name, title, author, publish_date,
                    retrieval_date, url, image_url, summary)
            )
    conn.commit()
    conn.close()

    return

# returns a comma seperated list of domains to be included for each category's search


def sourceListToString(sources_data):
    domains = ",".join([source["url"] for source in sources_data["sources"]])
    domains = domains.replace(
        "https://", "").replace("http://", "").replace("www.", "")
    return domains


if __name__ == '__main__':
    main()