CREATE_MOVIES_TABLE = """CREATE TABLE IF NOT EXISTS movies (
    title TEXT,
    release_timestamp REAL,
    watched INTEGER
); """

INSERT_MOVIES = (
    "INSERT INTO movies (title, release_timestamp, watched) VALUES (?, ?, 0);"
)

