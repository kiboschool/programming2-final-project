from event_brite_client import EventBriteAPIHelper

class Scheduler():
    def __init__(self):
        self.client = EventBriteAPIHelper()

    def schedule_tournament(self, tournament):
        for game in tournament.games:
            self.schedule_game(game)

    def schedule_game(self, game):
        event_id = self.client.create_event(game.name, str(game), game.start_time, game.end_time)
        game.event_id = event_id

    def update_game_event(self, game):
        self.client.update_event(game.event_id, game.name, str(game), game.start_time, game.end_time)
