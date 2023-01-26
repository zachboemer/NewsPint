import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Article, db
from datetime import datetime, time, timedelta

load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
    'postgres://', 'postgresql://', 1)
db.init_app(app)

# do some cors
CORS(app)


# do some jwt

# -------- ROUTES ---------

# get all articles - this is kinda just for testing, probably gonna remove


@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])


# returns the articles associated with the date -- if no date passed in, returns articles with the most recent retrieved_at date


@app.route('/pint-of-day/<date>', methods=['GET'])
@app.route('/pint-of-day/', methods=['GET'])
def get_pint_of_day(date=datetime.now().strftime('%Y-%m-%d')):
    if not is_valid_date(date):
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    today = datetime.now()
    currentTime = datetime.now()
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')

    # checks to see if you wanted today's results and that its after 5 PM
    if currentTime.hour < 17 and date is today:
        articles = Article.query.filter(Article.retrieval_date == yesterday)
    else:
        articles = Article.query.filter(Article.retrieval_date == date)
    return jsonify([article.to_dict() for article in articles])


# maybe routes for getting articles of a certain category
# also gotta add that column for category before we do that

def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

if __name__ == '__main__':
    app.run()
