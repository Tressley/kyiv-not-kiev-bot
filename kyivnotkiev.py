#!/usr/bin/python
import praw
import re
import os

#Create a new Reddit instance
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Windows:KyivNotKievBot:v0.3 (by /u/apollokami)",
    username="kyiv_not_kiev_bot",
)

#Set the subreddit to monitor
subreddit = reddit.subreddit("worldnews")

# First rodeo? Create an empty list
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

# If not, load the list of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

#Monitor all new comments for "Kiev"
for comment in subreddit.stream.comments(skip_existing=True):

    #If we haven't replied to this comment before
    if comment.id not in comments_replied_to:

        #Search for Kiev
        if re.search("Kiev", comment.body, re.IGNORECASE):
            #Reply to the comment
            kyiv_reply = u"\u0434\u043e\u0431\u0440\u0438\u0439\u0020\u0434\u0435\u043d\u044c!" + "\n\nUkrainians call their capital **Kyiv** (kee-yiv), the spelling, a transliteration of the Ukrainian \u041a\u0438\u0457\u0432." + "\n\n\u0421\u043b\u0430\u0432\u0430\u0020\u0423\u043a\u0440\u0430\u0457\u043d\u0456\u0021 🇺🇦" + "\n\n*****" + "\n\n^I ^am ^a ^bot. ^Please ^message ^my ^[developer](https://reddit.com/u/apollokami) ^to ^report ^an ^issue."
            comment.reply(kyiv_reply)
            print(comment.id)

            #Store the comment id
            comments_replied_to.append(comment.id)

            #Write our updated list back to the file
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")
