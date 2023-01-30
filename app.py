from crypt import methods
import os
import psycopg2
import pytz
import subprocess
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Article, db
from datetime import datetime, time, timedelta
from flask_httpauth import HTTPBasicAuth

load_dotenv()
auth = HTTPBasicAuth()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace(
    'postgres://', 'postgresql://', 1)
db.init_app(app)

# do some cors
CORS(app)

central = pytz.timezone('US/Central')
# do some jwt

# -------- ROUTES ---------

# get all articles - this is kinda just for testing, probably gonna remove
# @app.route('/articles', methods=['GET'])
# def get_articles():
#     articles = Article.query.all()
#     return jsonify([article.to_dict() for article in articles])


@app.route('/', methods=['GET'])
def index():
    return 'welcome to the backend'

# define authentication


@auth.get_password
def get_password(username):
    if username == os.environ['AUTH_USERNAME']:
        return os.environ['AUTH_PASSWORD']
    return None

# requires authentication


@app.route('/update-db', methods=['GET'])
@auth.login_required
def update_db():
    result = subprocess.run(["python", "update_db.py"], capture_output=True)
    return result.stdout


# returns the articles associated with the date -- if no date passed in, returns articles with the most recent retrieved_at date
@app.route('/pint-of-day/<date>', methods=['GET'])
@app.route('/pint-of-day/', methods=['GET'])
def get_pint_of_day(date=datetime.now(central).strftime('%Y-%m-%d')):
    if not is_valid_date(date):
        return jsonify({'error': 'Invalid date format. Please use YYYY-MM-DD.'}), 400

    today = datetime.now(central)
    yesterday = (today - timedelta(days=1)).strftime('%Y-%m-%d')
    print('date: ', date)
    print('today: ', today)
    # checks to see if you wanted today's results and that its after 5 PM
    if today.hour < 17 and date == today.strftime('%Y-%m-%d'):
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
