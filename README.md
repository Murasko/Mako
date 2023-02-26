# Mako

Discord Bot written in Python, using [pycord](https://github.com/Pycord-Development/pycord)

## Setup Working dir

Setup your working Directory with the following Commands
Windows:

```commandline
python -m venv venv
.\venv\Scripts\activate 
python -m pip install -r requirements.txt
```

Linux:

```commandline
python -m venv venv
source ./venv/bin/activate
python -m pip install -r requirements.txt
```

Create config.json and input the Streamers you want to get notified when live:

```
{
    "discord_token": "",
    "notification_channel": "",
    "twitch_client_id": "",
    "twitch_client_secret": "",
    "watchlist": [
        ""
    ]
}
```
