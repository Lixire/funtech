#!/usr/bin/env python3

import re
from datetime import datetime, date, timedelta
import sqlite3
from collections import defaultdict

from flask import Flask, jsonify, request, render_template, g

DATABASE = "funtech.db"

app = Flask(__name__, static_url_path="/static")

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def get_top_sentiment_companies(conn):
    company_scores = defaultdict(int)
    today = date.today()
    date_weights = {today - timedelta(days=days_ago): 1.0 / 2 ** days_ago for days_ago in range(7 + 1)}
    for tweet_date, company, average_sentiment in conn.execute("select date, company, sum(sentiment) / count(sentiment) from sentiments where date >= date('now', '-7 days') group by date, company"):
        date_value = datetime.strptime(tweet_date, "%Y-%m-%d").date()
        company_scores[company] += date_weights[date_value] * average_sentiment
    min_sentiment, max_sentiment = min(company_scores.values()), max(company_scores.values())
    if min_sentiment == max_sentiment: min_sentiment = max_sentiment - 1
    company_scores = [
        (company, (sentiment - min_sentiment) / (max_sentiment - min_sentiment))
        for company, sentiment in company_scores.items()
    ]
    return sorted(company_scores, key=lambda e: -e[1]) * 100

@app.route("/")
def index():
    top_sentiment_companies = get_top_sentiment_companies(get_db())
    return render_template(
        'index.html',
        trending_companies=top_sentiment_companies,
    )

if __name__ == "__main__":
    app.run(debug=True, port=8888) # debug mode
    #app.run(debug=False, host="0.0.0.0", port=80) # release mode - publicly visible
