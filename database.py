CREATE_POLLS = """CREATE TABLE IF NOT EXISTS polls
(id SERIAL PRIMARY KEY, title TEXT, owner_username TEXT);"""

CREATE_OPTIONS = """CREATE TABLE IF NOT EXISTS options
(id SERIAL PRIMARY KEY, option_text TEXT, poll_id INTEGER);"""

CREATE_VOTES = """CREATE TABLE IF NOT EXISTS votes
(username TEXT, option_id INTEGER);"""

SELECT_ALL_POLLS = "SELECT * FROM polls;"

SELECT_POLL_WITH_OPTIONS = """SELECT * FROM polls
JOIN options ON polls.id = options.poll_id
WHERE polls.id = %s;"""

INSERT_OPTION = "INSERT INTO options (option_text, poll_id) VALUES %s;"

INSERT_VOTE = "INSERT INTO votes (username, option_id) VALUES (%s, %s);"
