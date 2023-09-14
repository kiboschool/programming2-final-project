import math

from tournament import Tournament

import pdb

def starting_menu():
    print("*************************************************************")
    print("Welcome to our tournament management tool!")
    print("You can press '1' to create a new tournament")
    print("You can press '2' to edit the games of an existing tournament")
    print("You can press 'q' to quit")

    operation = input("What would you like to do? ")

    if operation == '1':
        tournament_setup()
    elif operation == '2':
        tournament_changes()
    elif operation == 'q':
        print("Thanks for usin our tool! exiting now...")
        exit()
    else:
        print("Unknown command, exiting now...")
        exit()

def tournament_setup():
    tournament_name = input("\nWhat would you like to call your tournament? ")
    tournament = Tournament(tournament_name)

    participant_count = request_integer_input("How many participants will enter this tournament? ")

    participants = gather_participants(participant_count)

    print("\nYour tournament is ready to be scheduled. Creating calendar invites now!")

    tournament.create_rounds(participants)
    print(f'{tournament=}')

    tournament.save()

    starting_menu()

# Must return a list of unique participants equal to the count
def gather_participants(count):
    participant_set = set()
    while len(participant_set) < count:
        new_participant = input("Please enter the name of the next participant: ")

        while new_participant in participant_set:
            new_participant = input("We already have registered this participant! please share a new name: ")

        participant_set.add(new_participant)

    return list(participant_set)


def tournament_changes():
    tournament_name = input("What tournament would you like to modify? ")

    try:
        tournament = Tournament.load_tournament(tournament_name)
    except:
        print("Could not find the tournament, try again!")
        starting_menu()

    if not tournament.has_games():
        print("The tournament we found has no games on record!, exiting")
        starting_menu()

    for i, game in enumerate(tournament.games):
        print(f'Press - {i} to edit {game}')

    game_id = -1
    while game_id < 0 or game_id >= len(tournament.games):
        game_id = request_integer_input("Please enter the id of the game you want to modify:  ")

    player_1 = input("Please enter the new player 1, or type enter not to change it: ")
    player_2 = input("Please enter the new player 2, or type enter not to change it: ")
    # date = input("Please enter the new date for the game, or type enter not to change it ")

    print("-----------------------")
    print("Saving your changes now")
    print("-----------------------")

    tournament.update_game(game_id, player_1, player_2)

    tournament.save()
    starting_menu()


def request_integer_input(message):
    int_input = input(message).strip()
    while not int_input.isnumeric():
        print("Sorry, please make sure to type in a number")
        int_input = input(message).strip()

    return int(int_input)


if __name__ == '__main__':
    starting_menu()
