import os
import json

from urllib import request
from event_brite_client import EventBriteAPIHelper

def schedule_tournament(tournament):
    for game in tournament.games:
        schedule_game(game)

def schedule_game(game):
    client = EventBriteAPIHelper()
    event_id = client.create_event(game.name, str(game), game.start_time, game.end_time)
    game.event_id = event_id

def update_game_event(game):
    client = EventBriteAPIHelper()
    client.update_event(game.event_id, game.name, str(game), game.start_time, game.end_time)

