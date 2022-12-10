import requests
import json
from datetime import datetime

with open("config.json") as config_file:
    config = json.load(config_file)

headers = {
    "Authorization": f"Bearer {config['twitch_access_token']}",
    "Client-Id": config["twitch_client_id"]
}

online_users = {}


def get_app_access_token():
    params = {
        "client_id": config["twitch_client_id"],
        "client_secret": config["twitch_client_secret"],
        "grant_type": "client_credentials"
    }

    response = requests.post("https://id.twitch.tv/oauth2/token", params=params)
    access_token = response.json()["access_token"]
    return access_token


def get_streams(users):
    params = {
        "user_id": users,
        "type": "live"
    }

    response = requests.get("https://api.twitch.tv/helix/streams", params=params, headers=headers)
    return {entry["user_login"]: entry for entry in response.json()["data"]}


def get_profile_picture(login_name):
    response = requests.get(f"https://api.twitch.tv/helix/users?id={login_name}", headers=headers)
    return response.json()["data"][0]["profile_image_url"]


def get_notifications():
    users = config["watchlist"]
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
