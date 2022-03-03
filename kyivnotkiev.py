#!/usr/bin/python
import praw
import re
import os
import time
from praw.exceptions import APIException
from datetime import datetime

# Create a new Reddit instance
reddit = praw.Reddit(
    client_id="",
    client_secret="",
    password="",
    user_agent="Windows:KyivNotKievBot:v0.8.7 (by /u/apollokami)",
    username="kyiv_not_kiev_bot",
)

# Set the subreddits to monitor
subreddit = reddit.subreddit("news+worldnews")

# First rodeo? Create an empty list file
if not os.path.isfile("comments_replied_to.txt"):
    comments_replied_to = []

# If not, load the list file of posts we have replied to
else:
    # Read the file into a list and remove any empty values
    with open("comments_replied_to.txt", "r") as f:
        comments_replied_to = f.read()
        comments_replied_to = comments_replied_to.split("\n")
        comments_replied_to = list(filter(None, comments_replied_to))

# Monitor all new comments
for comment in subreddit.stream.comments():

    # If we haven't replied to this comment before and it's not our bot
    if comment.id not in comments_replied_to and comment.author != "kyiv_not_kiev_bot":

        # Try searching for "Kiev" and replying to a comment
        try:
            if re.search("Kiev", comment.body, re.IGNORECASE) and not re.search("Kyiv", comment.body, re.IGNORECASE):
                # Reply to the comment
                kyiv_reply = u"\u0434\u043e\u0431\u0440\u0438\u0439\u0020\u0434\u0435\u043d\u044c,\n\n" + "As part of the KyivNotKiev campaign, Ukraine asks that their capital be called _**Kyiv**_ (/ki\u003av/ KEEV) (derived from the Ukrainian language name \u041a\u0438\u0457\u0432) instead of _Kiev_ (derived from the Russian language name).\n\n" + "> The \u0022KyivNotKiev\u0022 campaign is part of the broader \u0022CorrectUA\u0022 campaign, which advocates a change of name in English; not only for Kyiv, but also for other Ukrainian cities whose English names are derived from Russian as well." + "\n\n*****\n\n" + "^I ^am ^a ^bot ^hoping ^to ^educate. ^\uff5c ^Read ^more ^about ^the [^KyivNotKiev](https://en.wikipedia.org/wiki/KyivNotKiev) ^campaign. ^\uff5c " + "[^Support ^Ukraine](https://www.reddit.com/r/ukraine/comments/s6g5un/want_to_support_ukraine_heres_a_list_of_charities/) ^\uff5c " + "^\u0421\u043b\u0430\u0432\u0430 ^\u0423\u043a\u0440\u0430\u0457\u043d\u0456\u0021 ^🇺🇦"
                comment.reply(kyiv_reply)
                # Get the current time
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                # Log the comment ID and time of reply
                print(current_time + str(": ") + comment.id)

                # Store the comment ID
                comments_replied_to.append(comment.id)

                # Write our updated list back to the file
                with open("comments_replied_to.txt", "a") as f:
                    f.write(comment.id + "\n")

                # Wait 15 minutes before trying again so we don't spam
                time.sleep(900)
        
        # Log the exception preventing us from posting
        except APIException as e:
            warning_emoji = u"\u26A0 "
            print(warning_emoji + str(e))
            # Wait a minute before trying again
            time.sleep(60)
