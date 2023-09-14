import json

from datetime import timedelta
from math import ceil, log, floor

from game import Game

class Tournament:
    def __init__(self, name, games = None):
        self.name = name
        # self.start_date = start_date

        self.interval = 2
        self.games = [] if games is None else games

    def create_rounds(self, participants):
        # If participants are not a power of 2, panick!
        if not power_of_two(len(participants)):
            raise RuntimeError("The number of participants must be a power of two!")

        # We go over each "round" of the competition, and we create all the games in that round.
        # Knowing the round lets us name the games correctly: The last round is the finals
        # The round before last is the semi-finals

        # Initially, the number of games is equal to half the number of participants
        # Each time through the loop, we will divide this by 2, until we get to 1 game in the round
        games_in_round = len(participants) // 2

        rounds_count = 0
        while games_in_round > 0:
            round_name = compute_round_name(games_in_round)

            for game_count in range(games_in_round):
                game_name = f'{round_name} Game {game_count + 1}'
                # game_date = self.start_date + timedelta(days = rounds_count * self.interval)

                if rounds_count == 0:
                # The first round is special because we know all the competitors, so we should include them in the game
                    player_1 = participants[2*game_count]
                    player_2 = participants[2*game_count + 1]
                    self.games.append(Game(game_name, player_1, player_2))
                else:
                    self.games.append(Game(game_name))

            rounds_count += 1
            games_in_round  //= 2

    def __repr__(self):
        # return f'{self.name} - {self.start_date}\n{self.games}'
        return f'{self.name} \n{self.games}'

    def has_games(self):
        return len(self.games) > 0

    def save(self):
        with open(f'{self.name}.games', 'w') as games_record:
            for game in self.games:
                games_record.write(game.to_json_string())
                games_record.write('\n')

    @staticmethod
    def load_tournament(tournament_name):
        games = []
        with open(f'{tournament_name}.games', 'r') as games_record:
            for line in games_record:
                games.append(Game.from_json_string(line))

        return Tournament(tournament_name,games)

    def update_game(self, game_id, player_1, player_2, date = None):
        self.games[game_id].update(player_1, player_2, date)

def power_of_two(value):
    return (ceil(log(value, 2)) == floor(log(value, 2)))

# Helper functions
def get_rounds_for_players(player_count):
    return int(log(player_count, 2))

def compute_round_name(game_count):
    input_type = type(game_count)
    if input_type is int or input_type is float or (input_type is str and game_count.isnumeric()):
        if int(game_count) == 1:
            return 'Final'
        if int(game_count) == 2:
            return 'Semi-Finals'
        if int(game_count) == 4:
            return 'Quarter-Finals'

        return f'Round of {game_count * 2}'

    raise TypeError(f"{game_count} must be a number or a string we can convert to a number")

if __name__ == '__main__':
    participants = ['a', 'b', 'c', 'd']

    t = Tournament("test tourney")
    t.create_rounds(participants)

    print(t)

    print(t.to_json_string())