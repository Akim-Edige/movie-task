class CinemaTicketSystem:
    def __init__(self):
        self.movies = []
        self.tickets = {}

    def addMovie(self, movieName):
        self.movies.append(movieName)
        return len(self.movies)


    def buyTicket(self, user_id, movie_id):
        self.tickets[user_id] = movie_id


    def cancelTicket(self, user_id):
        del self.tickets[user_id]
