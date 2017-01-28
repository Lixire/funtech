#!/usr/bin/env python3

import re
from datetime import datetime, date, timedelta
import sqlite3

from flask import Flask, jsonify, request, render_template

# set up application
app = Flask(__name__, static_url_path="/static")
conn = sqlite3.connect("funtech.db")

def get_top_sentiment_companies(conn):
    company_scores = {}
    today = date.today
    date_weights = {today - timedelta(days=days_ago): 1.0 / 2 ** days_ago for days_ago in range(7 + 1)}
    for tweet_date, company, average_sentiment in con.execute("select date, company, sum(sentiment) / count(sentiment) from measurements where date >= date('now', '-1 week') group by date, company"):
        date_value = date(*tweet_date.split("-"))
        company_scores[company] += date_weights[date_value] * average_sentiment
    companies = sorted(company_scores.items(), key=lambda e: -e[1])
    return companies

@app.route("/")
def index():
    top_sentiment_companies = get_top_sentiment_companies(conn)
    return render_template('index.html', trending_companies = top_sentiment_companies)

if __name__ == "__main__":
    app.run(debug=True, port=8888) # debug mode
    #app.run(debug=False, host="0.0.0.0", port=80) # release mode - publicly visible
