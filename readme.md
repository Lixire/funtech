# Sentigrade
By: Amy Qiu (amylyn.qiu@gmail.com), Anthony Zhang (azhang9@gmail.com)

## Inspiration
Inspired by the fintech challenge. We wanted to explore possible ways large-scale social trends could influence the market.

## What it does
Sentigrade is constantly listening to tweets and analyzing the sentiments of messages about different companies. Over time, it builds up an idea of which companies are viewed positively, and which negatively.

Sentigrade also shows historical stock data, allowing users to look for potential relations.

## How we built it

A service constantly updates the database with information from the real-time Twitter message stream. It performs sentiment analysis and aggregates the result over fixed intervals.

The web backend, written in Flask, pulls Twitter data from the database and stock data from Yahoo Finance. The frontend is a simple jQuery/Bootstrap page to display the results in an informative, nice-looking way.

## Challenges we ran into

We originally intended to use arbitrary lists of items, retrieving every message from Twitter. However, this functionality was not available. Also, the stock data retrieval proved messy, though it worked well in the end.

## Accomplishments that we're proud of

Finishing the project ahead of schedule and getting to really flesh out the details.

## What we learned

Web development is scary to start with since you don't know where to begin, but once you hash out all the details, everything comes through.

## What's next for Sentigrade

Sentiment history. Actionable insights, possibly. Per-user settings for filtering, etc.
