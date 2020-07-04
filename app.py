import datetime
import database

menu = """Please select one of the following options:
1) Add new movie.
2) View upcoming movies.
3) View all movies
4) Watch a movie
5) View watched movies.
6) Exit.

Your selection: """
welcome = "Welcome to the watchlist app!"


print(welcome)
database.create_tables()


def prompt_add_movie():
    """
    Prompt a user to add new movie
    """
    title = input("Movie title: ")
    release_date = input("Release date (dd-mm-YYYY): ")
    parsed_date = datetime.datetime.strptime(release_date, "%d-%m-%Y")
    timestamp = parsed_date.timestamp()

    database.add_movie(title, timestamp)


def print_movie_list(heading, movies):
    """
    Print list of upcoming movies
    """
    print(f"-- {heading} Movies --")
    for _id, title, release_date in movies:
        movie_date = datetime.datetime.fromtimestamp(release_date)
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{_id}: {title} (on {human_date})")
    print("--- \n")


def print_watched_movie_list(username, movies):
    print(f"-- {username}'s watched movies --")
    for movie in movies:
        print(f"{movie[1]}")
    print("---- \n")


def prompt_watch_movie():
    """
    Mark a movie as watched
    """
    username = input("Username: ")
    movie_title = input("Enter movie title you've watched: ")
    database.watch_movie(username, movie_title)


user_input = input(menu)

while user_input != "6":
    if user_input == "1":
        prompt_add_movie()
        user_input = input(menu)
    elif user_input == "2":
        movies = database.get_movies(True)
        print_movie_list("Upcoming", movies)
        user_input = input(menu)
    elif user_input == "3":
        movies = database.get_movies()
        print_movie_list("All", movies)
        user_input = input(menu)
    elif user_input == "4":
        prompt_watch_movie()
        user_input = input(menu)
    elif user_input == "5":
        username = input("Username: ")
        movies = database.get_watched_movies(username)
        print_watched_movie_list(username, movies)
    else:
        print("Invalid input, please try again!")
