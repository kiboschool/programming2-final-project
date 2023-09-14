import json
from datetime import datetime, timedelta

# Make this serialized already. This is the example they can 
# redo this for the tournament class

class Game:
    def __init__(self, game_name, player_1 = 'Unknown', player_2 = 'Unknown'):
        self.name = game_name
        # self.date = str(game_date)
        self.player_1 = player_1
        self.player_2 = player_2

    def __repr__(self):
        # description = f'{self.name} - {self.date}: {self.player_1} VS {self.player_2}'
        # return f'{self.date}: {self.player_1} VS {self.player_2}'
        return f'{self.name}: {self.player_1} VS {self.player_2}'

    def update(self, player_1, player_2, date = None):
        if player_1 != '':
            self.player_1 = player_1
        if player_2 != '':
            self.player_2 = player_2

    def to_json_string(self):
        # return json.dumps({'game_name': self.name, 'game_date': self.date, 'player_1': self.player_1, 'player_2': self.player_2})
        return json.dumps({'game_name': self.name, 'player_1': self.player_1, 'player_2': self.player_2})

    @staticmethod
    def from_json_string(input_string):
        game_dict = json.loads(input_string)
        return Game(game_dict.get('game_name'), game_dict.get('player_1'), game_dict.get('player_2'))

if __name__ == '__main__':
    g = Game('Final', 'Barca', 'Messi')
    print(g)
    print(g.to_json_string())

    g2 = Game.from_json_string('{"game_name": "Final", "player_1": "Barca", "player_2": "Madrid"}')
    print(g2)