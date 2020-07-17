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
