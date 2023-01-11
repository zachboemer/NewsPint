#!/bin/bash

cd client/news-pint
npm install
npm run build

cd ../../server
pipenv install
pipenv shell
python app.py