#!/usr/bin/env python
import requests
import json
import re

def cleanComments(comments):
    comments = re.sub(r'\n', ' ', comments)
    # comebacksis is the reason for the long regex
    comments = re.sub(r'(https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&\/=]*)|(\<wbr\>[-a-zA-Z0-9()@:%_\+.~#?&\/=]*))|(youtu.be\/-?\w+)|(\d+)|([^a-zA-Z ])', '', comments)
    # print(comments.split())
    return comments

threadInt = 105594331
threadNum = "105594331"
r = requests.get(f'https://desuarchive.org/_/api/chan/thread/?board=mu&num={threadInt}')
thread = r.json()
# print(thread)
posts = thread[threadNum]['posts']
comments = ''
for post in posts.keys():
    comments += posts[post]["comment_sanitized"] + '\n'

cleanedComments = cleanComments(comments)
cleanedComments = cleanedComments.split()
# print(cleanedComments)

# r = r.json()[thread]['op']['exif']
# print(int(json.loads(r)['uniqueIps']))
