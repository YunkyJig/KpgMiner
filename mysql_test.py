#!/usr/bin/env python
from dotenv import load_dotenv
import requests
import json
import os
import mysql.connector
# https://askubuntu.com/questions/1249973/connect-mysql-workbench-to-wsl2
mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=os.environ.get("db_password"),
  database="archive_no_stopwords"
)

cursor = mydb.cursor()

id = 5
post_date = 1598843426
data_timestamp = 1598843426
total_posts = 1
total_images = 2
unique_ips = 2


thread_id = 5
word = "croatrocket"
occurences = 10

print("INSERT INTO threads"
            f"VALUES({id}, FROM_UNIXTIME({post_date}), FROM_UNIXTIME({data_timestamp}), {total_posts}, {total_images}, {unique_ips})")

thread = "105594331"
r = requests.get(f'https://desuarchive.org/_/api/chan/thread/?board=mu&num={thread}')
r = r.json()
exif = r[thread]['op']['exif']
unique_ips = int(json.loads(exif)['uniqueIps'])
id = int(r[thread]['op']['num'])

# Need to include the column names for it to work
# addThread = ("INSERT INTO threads (id, post_date, unique_ips)"
#             f"VALUES({id}, FROM_UNIXTIME({post_date}), {unique_ips})"
#             )


# cursor.execute(addThread)

# addWord = ("INSERT INTO words (thread_id, word, occurences)"
#             f"VALUES({thread_id}, \"{word}\", {occurences})"
#             )


# multiple lines insert
addWord = "INSERT INTO words (thread_id, word, occurences)"

for i in range(5):
  if i == 0:
    addWord += f"VALUES({id}, \"{word}\", {occurences})"
  else:
    addWord += f",({id}, \"{word}\", {occurences})"



cursor.execute(addWord)

mydb.commit()

cursor.close()
mydb.close()