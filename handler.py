import json
import requests
from os import environ
from bs4 import BeautifulSoup

def webhook(event, context):
    DISCORD_WEBHOOK_URL = environ.get("DISCORD_WEBHOOK_URL")
    DISCORD_ROLE_ID = environ.get("DISCORD_ROLE_ID")

    return_obj = {
        "statusCode": 200,
        "body": json.dumps({ "executed": False })
    }

    soup = BeautifulSoup(event["body"])
    entry = soup.entry

    if not entry:
        return_obj["body"] = json.dumps({ "executed": False, "error": "No entry found" })
        return return_obj

    title = entry.title
    link = entry.find("link", rel="alternate")
    channel = entry.author.id

    return_obj["body"] = json.dumps({ "executed": False, "title": title.string })

    mention_str = ('@everyone, ' if DISCORD_ROLE_ID == 'everyone' else '<@&' + DISCORD_ROLE_ID + '>, ')

    data = {
        "content": "Hey " + mention_str + "**" + channel.string + "** just uploaded a video! Check out '" + title.string + "' here:\n" + link.get("href"),
        "username": channel.string,
        "avatar_url": "https://avatar.glue-bot.xyz/youtube-avatar/q?url=" . link.get("href")
    }

    result = requests.post(DISCORD_WEBHOOK_URL, json = data)

    try:
        result.raise_for_status()
    except requests.exceptions.HTTPError as err:
        return_obj["body"] = json.dumps({ "executed": False, "error": "discord webhook returned an error. " + err })
    else:
        return_obj["body"] = json.dumps({ "executed": True })

    return return_obj
