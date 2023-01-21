import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from models import Article, db

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
def get_pint_of_day(date):
    # TODO
    return {}

# maybe routes for getting articles of a certain category
# also gotta add that column for category before we do that


if __name__ == '__main__':
    app.run()
