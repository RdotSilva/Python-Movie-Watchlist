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
