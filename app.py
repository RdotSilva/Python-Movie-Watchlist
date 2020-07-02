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
    for movie in movies:
        movie_date = datetime.datetime.fromtimestamp(movie[1])
        human_date = movie_date.strftime("%b %d %Y")
        print(f"{movie[0]} (on {human_date})")
    print("--- \n")


def prompt_watch_movie():
    """
    Mark a movie as watched
    """
    movie_title = input("Enter movie title you've watched: ")
    database.watch_movie(movie_title)


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
        movies = database.get_watched_movies()
        print_movie_list("Watched", movies)
        user_input = input(menu)
    elif user_input == "5":
        pass
    else:
        print("Invalid input, please try again!")
