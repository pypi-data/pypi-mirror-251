# WORK IN PROGRESS

This library is still a wip and is far from ready to be used. Feel free to use but expect breaking changes if you don't lock a version.

# Battlefy.py 
A Python Library for Battlefy.com

Battlefy.py is an asyncio library for accessing information off of Battlefy.com.

This library has been designed for use by IPL for Splatoon tournaments primarily. 

## Installation
```sh
pip install battlefy.py
```

## Usage

### Tournaments
```py
from battlefy import TournamentClient

client = TournamentClient(headers = {})

tour_id = "5d167f61ddd2f83f429dc858"
tournament = await client.get_tournament(tour_id)

print(tournament.name)
```