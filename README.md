# MuraskoBot
Discord Bot written in Python

Using [pycord](https://github.com/Pycord-Development/pycord)

## Setup Working dir
Create the venv with the needed packages
```
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Create .env File and add Discord Bot token
```
echo "TOKEN='insertTokenHere'" > .env
```

Create Bot Executable
```
pyinstaller -F --clean -y --workpath build --distpath dist muraskobot.py
```