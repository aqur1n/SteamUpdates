[![Latest release](https://img.shields.io/github/v/release/aqur1n/SteamUpdates?include_prereleases&label=Latest%20Release&logo=github&sort=semver&style=for-the-badge&logoColor=white)](https://github.com/aqur1n/SteamUpdates/releases)
[![Python version](https://img.shields.io/badge/Python-3.9-green?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/downloads/release/python-390/)

# SteamUpdates
Get updated branches of your game in steam
## Installation
1. Download the latest Python 3.9 security bugfix
2. Download the latest version or the main branch and unzip the archive to a convenient location
3. Open the console (Windows), use the commands to navigate to the directory with main.py and run python using the command:
```
python3.9 main.py
```

## Set up config.json
1. Create a file in the directory with `main.py` with the name `config.json`
2. Copy the configuration example from below and customize it for yourself
```
{
    "app_id": STEAM_APP_ID,
    "discord_webhook_url": "DISCORD_WEBHOOK_URL"
}
```
