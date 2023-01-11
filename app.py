import os
import psycopg2

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
# from newsapi import NewsApiClient

load_dotenv()
db_url = os.environ['DATABASE_URL']
conn = psycopg2.connect(db_url, sslmode='require')

app = Flask(__name__, static_folder='client/news-pint/build',
            static_url_path='/')


@app.route('/')
def index():
    return app.send_static_file('index.html')

# more routes here


if __name__ == '__main__':
    app.run()
    app.run()
