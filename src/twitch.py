import os
import requests
import json
from datetime import datetime

from dotenv import load_dotenv

with open("config.json") as cfile:
    config = json.load(cfile)

load_dotenv()

__headers = {
    "Authorization": f"Bearer {os.environ['ACCESS_TOKEN']}",
    "Client-Id": os.environ["CLIENT_ID"]
}


def get_app_access_token():
    params = {
        "client_id": os.environ["CLIENT_ID"],
        "client_secret": os.environ["CLIENT_SECRET"],
        "grant_type": "client_credentials"
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", params=params)
    access_token = response.json()["access_token"]
    return access_token


def get_users(login_names):
    params = {
        "login": login_names
    }

    headers = __headers

    response = requests.get("https://api.twitch.tv/helix/users", params=params, headers=headers)
    return {entry["login"]: entry["id"] for entry in response.json()["data"]}


def get_streams(users):
    params = {
        "user_id": users.values()
    }

    headers = __headers

    response = requests.get("https://api.twitch.tv/helix/streams", params=params, headers=headers)
    return {entry["user_login"]: entry for entry in response.json()["data"]}


def get_profile_pictures(userid):
    headers = __headers
    response = requests.get(f"https://api.twitch.tv/helix/users?id={userid}", headers=headers)
    return response.json()["data"][0]["profile_image_url"]


online_users = {}


def get_notifications():
    users = get_users(config["watchlist"])
    streams = get_streams(users)

    notifications = []
    for user in users:
        if user not in online_users:
            online_users[user] = datetime.utcnow()

        if user not in streams:
            online_users[user] = None
        else:
            started_at = datetime.strptime(
                streams[user]["started_at"], "%Y-%m-%dT%H:%M:%SZ")
            if online_users[user] is None or started_at > online_users[user]:
                notifications.append(streams[user])
                online_users[user] = started_at

    return notifications
