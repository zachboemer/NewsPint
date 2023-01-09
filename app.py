from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

#more routes here

if __name__ == '__main__':
    app.run()
    app.run()