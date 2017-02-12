#!/usr/bin/env python3

import sqlite3
from datetime import date, timedelta
from os import path

# run `crontab -e` to edit the cron settings
# edit it to have the following line at the end: `0 0 * * *    python /home/ubuntu/cleanup.py`

DATABASE_FILE = path.join(path.dirname(path.abspath(__file__)), "funtech.db")

conn = sqlite3.connect(DATABASE_FILE)

conn.execute("CREATE TABLE IF NOT EXISTS sentiments (date TEXT, company TEXT, sentiment FLOAT)")

dat = str(date.today() - timedelta(days=14))
conn.execute("delete from sentiments where date < ?", (dat,))
conn.commit()
conn.close()
