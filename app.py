import os
import psycopg2
from psycopg2.errors import DivisionByZero
from dotenv import load_dotenv
import database

DATABASE_PROMPT = "Enter the DATABASE_URI value or leave empty to load from .env file: "

MENU_PROMPT = """-- Menu --

1) Create new poll
2) List open polls
3) Vote on a poll
4) Show poll votes
5) Select a random winner from a poll option
6) Exit

Enter your choice: """

NEW_OPTION_PROMPT = "Enter new option text (or leave empty to stop adding options): "


def prompt_create_poll(connection):
    """
    Prompt user to create a poll
    """
    poll_title = input("Enter poll title: ")
    poll_owner = input("Enter poll owner: ")
    options = []

    new_option = input(NEW_OPTION_PROMPT)

    while len(new_option) != 0:
        options.append(new_option)
        new_option = input(NEW_OPTION_PROMPT)

    database.create_poll(connection, poll_title, poll_owner, options)


def list_open_polls(connection):
    """
    Print open polls
    """
    polls = database.get_polls(connection)

    for _id, title, owner in polls:
        print(f"{_id}: {title} (created by {owner})")


def prompt_vote_poll(connection):
    """
    Prompt user to vote on a poll
    """
    poll_id = int(input("Enter poll would you like to vote on: "))

    poll_options = database.get_poll_details(connection, poll_id)
    print_poll_options(poll_options)

    option_id = int(input("Enter option you'd like to vote for: "))
    username = input("Enter the username you'd like to vote as: ")
    database.add_poll_vote(connection, username, option_id)


def print_poll_options(poll_with_options):
    """
    Print all poll options
    """
    for option in poll_with_options:
        print(f"{option[3]}: {option[4]}")


def show_poll_votes(connection):
    """
    Prompt user to select what poll they want to see votes for and list the votes
    """
    poll_id = int(input("Enter poll you would like to see votes for: "))
    try:
        # This gives us count and percentage of votes for each option in a poll
        poll_and_votes = database.get_poll_and_vote_results(connection, poll_id)
    except DivisionByZero:
        print("No votes yet cast for this poll.")
    else:
        for _id, option_text, count, percentage in poll_and_votes:
            print(f"{option_text} got {count} votes ({percentage:.2f}% of total)")


def randomize_poll_winner(connection):
    """
    Pick a randomly selected winner from a poll
    """
    poll_id = int(input("Enter poll you'd like to pick a winner for: "))
    poll_options = database.get_poll_details(connection, poll_id)
    _print_poll_options(poll_options)

    option_id = int(
        input(
            "Enter which is the winning option, we'll pick a random winner from voters: "
        )
    )
    winner = database.get_random_poll_vote(connection, option_id)
    print(f"The randomly selected winner is {winner[0]}.")

