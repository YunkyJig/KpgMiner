#!/usr/bin/env python


# Script for filling database with mock data so query times can be tested

from dotenv import load_dotenv
import mysql.connector
import sys
import os


mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=os.environ.get("db_password"),
  database="archive_no_stopwords"
)
cursor = mydb.cursor()

cursor.execute("SELECT * FROM threads")
myresult = cursor.fetchall()
# print(myresult[0][0])

# sys.exit()

data = open("cleanData2.txt", "r")
data = data.read()
data = data.lower()


# last one was 120
for i, row in enumerate(myresult):
    if i < 120:
        continue

    thread_id = row[0]
    wordCount = {}
    for word in data.split():
        if len(word) > 50:
            continue
        
        word = word.lower()
        if word in wordCount:
            wordCount[word] += 1
        else:
            wordCount[word] = 1

    addWord = "INSERT INTO words (thread_id, word, occurences)"
    for j, word in enumerate(wordCount.keys()):
        if j == 0:
            addWord += f"VALUES({thread_id}, \"{word}\", {wordCount[word]})"
        else:
            addWord += f",({thread_id}, \"{word}\", {wordCount[word]})" 

    if addWord != "INSERT INTO words (thread_id, word, occurences)":
        cursor.execute(addWord)
        mydb.commit()

    print(i)


cursor.close()
mydb.close()