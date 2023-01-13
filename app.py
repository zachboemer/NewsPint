import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import db, Article
# from newsapi import NewsApiClient

load_dotenv()
app = Flask(__name__)
db_url = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db.init_app(app)


# get all articles
@app.route('/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])

# more routes here


if __name__ == '__main__':
    app.run()
    app.run()
