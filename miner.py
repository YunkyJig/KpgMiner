#!/usr/bin/env python
from os import error
from dotenv import load_dotenv
import requests
import re
import os
import sys
import json
import mysql.connector
import time


load_dotenv()


def storeWords():
    pass

def cleanComments(comments):
    comments = re.sub(r'\n', ' ', comments)
    # comebacksis is the reason for the long regex
    comments = re.sub(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)|(\<wbr\>[-a-zA-Z0-9()@:%_\+.~#?&\/=]*))|(youtu.be\/-?\w+)|(\d+)|([^a-zA-Z ])', '', comments)
    # print(comments.split())
    return comments

def fetchThread(threadNum):
    # http.client.RemoteDisconnected: Remote end closed connection without response
    # Sometimes a http.client.RemoteDisconnected will occur, so loop until its successful
    serverError = True
    threadData = {}
    while(serverError):
        try:
            threadData = requests.get(f'https://desuarchive.org/_/api/chan/thread/?board=mu&num={threadNum}')
            threadData = threadData.json()
            serverError = False
        except:
            sleepTime = 2.5
            print(f'Request to thread was unsuccessful. Trying again in {sleepTime} seconds')
            time.sleep(sleepTime)

    return threadData

def addWordsToDB(threadData, threadNum, thread_id):
    print('getting words')
    posts = threadData[threadNum]['posts']
    comments = ''
    for post in posts.keys():
        comments += posts[post]["comment_sanitized"] + '\n'

    cleanedComments = cleanComments(comments)

    cleanedComments = cleanedComments.split()
    wordCount = {}

    for word in cleanedComments:
        if len(word) > 50:
            continue
        
        word = word.lower()
        if word in wordCount:
            wordCount[word] += 1
        else:
            wordCount[word] = 1

    addWord = "INSERT INTO words (thread_id, word, occurences)"
    for i, word in enumerate(wordCount.keys()):
        if i == 0:
            addWord += f"VALUES({thread_id}, \"{word}\", {wordCount[word]})"
        else:
            addWord += f",({thread_id}, \"{word}\", {wordCount[word]})" 
    
    # sometimes there are no words in any post like thread no.105242612
    if addWord != "INSERT INTO words (thread_id, word, occurences)":
        cursor.execute(addWord)
        mydb.commit()

def main():
    for page in range(35, 36):
        threads = requests.get(f'https://desuarchive.org/_/api/chan/search/?subject=\"KPOP GENERAL\"&board=mu&start=2021-04-01&end=2021-04-30&page={page}')
        threads = threads.json()
        
        # Error will always be reached once there are no more threads available in the time range
        if 'error' in threads:
            error = threads['error']
            print(f'Error occured with search api: {error}')
            print('Exiting')
            sys.exit(1)

        t0 = time.time()
        for i, thread in enumerate(threads['0']['posts']):
            # Keep the if statement commented out in case connection ends before fetching all
            # threads
            # if i < 19:
            #     continue

            threadNum = thread['thread_num']
            print('Thread num:', threadNum)
            print('i:', i)

            threadData = fetchThread(threadNum)

            # Sleeping to slow down the request rate. Was fetching nearly 3 threads a second
            time.sleep(1.0)

            if 'error' in threadData:
                error = threadData['error']
                print(f'Error occured with search api: {error}. Skipping.')
                continue
            # Sometimes desuarchives will archive a thread with no posts
            if 'posts' not in threadData[threadNum]:
                continue
            
            thread_id = int(threadNum)
            unique_ips = int(json.loads(threadData[threadNum]["op"]["exif"])['uniqueIps'])
            post_date = threadData[threadNum]["op"]["timestamp"]
            addThread = ("INSERT INTO threads (id, post_date, unique_ips)"
                f"VALUES({thread_id}, FROM_UNIXTIME({post_date}), {unique_ips})"
            )   

            try:
                cursor.execute(addThread)
                mydb.commit()
                print('thread added')
            except mysql.connector.errors.IntegrityError:
                print('thread was already in database. continuing')
                continue
            
            addWordsToDB(threadData, threadNum, thread_id)
        
        # Keep this here to ensure that the search api rate limit(5 requests per minute) isn't exceeded
        time.sleep(2.0)
        
        t1 = time.time()
        total = t1-t0
        print('total time for page', page, ":", total)
        print('page', page, 'done')
        

mydb = mysql.connector.connect(
  host="127.0.0.1",
  user="root",
  password=os.environ.get("db_password"),
  database="archive_no_stopwords"
)
cursor = mydb.cursor()

main()

cursor.close()
mydb.close()
