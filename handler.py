try:
  import unzip_requirements
except ImportError:
  pass

from distutils.util import strtobool
import json
import requests
from os import environ
from bs4 import BeautifulSoup

# handle the websub challenge protocol
def challenge(event, context):
    # reject challenge requests without a challenge string, a topic, or a non youtube topic
    if 'hub.challenge' not in event["queryStringParameters"] or 'hub.topic' not in event["queryStringParameters"] or not event["queryStringParameters"]['hub.topic'].startswith("https://www.youtube.com/xml/feeds/videos.xml?channel_id="):
        return { "statusCode": 404 }

    challenge = event["queryStringParameters"]["hub.challenge"]
    topic_url = event["queryStringParameters"]["hub.topic"]
    print("[youtube-websub] challenge received: " + challenge + " for topic: " + topic_url)


    return { "statusCode": 200, "body": event["queryStringParameters"]["hub.challenge"] }

def webhook(event, context):
    DISCORD_WEBHOOK_URL = environ.get("DISCORD_WEBHOOK_URL")
    DISCORD_ROLE_ID = environ.get("DISCORD_ROLE_ID", "everyone")
    INCLUDE_SHORTS_UPLOADS = strtobool(environ.get("INCLUDE_SHORTS_UPLOADS", "True"))

    return_obj = {
        "statusCode": 200,
        "body": json.dumps({ "executed": False })
    }

    # don't define lxml - pain in the butt to set up with AWS because of
    # c dependency
    # also https://forum.serverless.com/t/13652
    soup = BeautifulSoup(event["body"])
    entry = soup.entry

    if not entry:
        return_obj["body"] = json.dumps({ "executed": False, "error": "No entry found" })
        return return_obj

    print("[youtube-websub] entry recieved: " + str(entry))

    title = entry.title.string
    link = entry.find("link", rel="alternate")
    channel = entry.author.find('name').string

    if not INCLUDE_SHORTS_UPLOADS and "#shorts".casefold() in title.casefold():
        print("[youtube-websub] Skipped due to rule: INCLUDE_SHORTS_UPLOADS === False")
        return_obj["body"] = json.dumps({ "executed": True, "title": title })
        return return_obj

    return_obj["body"] = json.dumps({ "executed": False, "title": title })

    mention_str = ('@everyone, ' if DISCORD_ROLE_ID == 'everyone' else '<@&' + DISCORD_ROLE_ID + '>, ')

    data = {
        "content": "Hey " + mention_str + "**" + channel + "** just uploaded a video! Check out '" + title + "' here:\n" + link.get("href"),
        "username": channel,
        "avatar_url": "https://avatar.glue-bot.xyz/youtube-avatar/q?url=" + link.get("href")
    }

    result = requests.post(DISCORD_WEBHOOK_URL, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return_obj["body"] = json.dumps({ "executed": False, "error": "discord webhook returned an error. " + err })
    else:
        return_obj["body"] = json.dumps({ "executed": True })

    return return_obj
