import sqlite3
from datetime import date, timedelta

# run `crontab -e` to edit the cron settings
# edit it to have the following line at the end: `0 0 * * *    python /home/ubuntu/cleanup.py`

conn = sqlite3.connect('funtech.db')

conn.execute("CREATE TABLE IF NOT EXISTS sentiments (date TEXT, company TEXT, sentiment FLOAT)")

dat = str(date.today() - timedelta(days=14))
conn.execute("delete from sentiments where date < ?", (dat,))
