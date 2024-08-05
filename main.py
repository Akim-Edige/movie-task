from cinema import CinemaTicketSystem
from flask import Flask, render_template, request

cinemaSystem = CinemaTicketSystem()

app = Flask(__name__)

db = {"user1":"admin"}
movies_db = cinemaSystem.movies
tickets = cinemaSystem.tickets

cinemaSystem.addMovie("Cars")
cinemaSystem.addMovie("House of Dragons")
cinemaSystem.addMovie("Interstellar")

currentUser = ''

@app.route('/')
def initial():
    return render_template("login.html")


@app.route('/login', methods=["POST"])
def home():
    global currentUser
    login = request.form["login"]
    password = request.form["password"]

    if login in db:
        if db[login]==password:
            currentUser = login
            return render_template("index.html", userName=currentUser)
        else:
            return render_template("login.html", alert = True)
    else:
        return render_template("login.html", alert = True)

@app.route('/main')
def main():
    global currentUser
    return render_template("index.html", userName=currentUser)


@app.route('/registerPage')
def rega():
    return render_template("register.html", alert=False)


@app.route('/registerAction', methods=["POST"])
def addUser():
    login = request.form["login"]
    password = request.form["password"]

    if login in db:
        return render_template("register.html", alert = True, success = False)
    else:
        db[login]=password
        return render_template("register.html", alert = True, success = True)

@app.route('/addNewMovieForm')
def addMovieForm():
    return render_template("addmovie.html", movieList=movies_db)

@app.route('/addNewMovie', methods=["POST"])
def addMovie():
    global currentUser
    movieName = request.form["movieName"]
    cinemaSystem.addMovie(movieName)
    return render_template("index.html", userName=currentUser)

@app.route('/showMovie')
def show():
    return render_template("showMovie.html", movieList=movies_db, dbLength = len(movies_db))

@app.route('/buyTicket')
def buy():
    return render_template("buy.html", movieList=movies_db, dbLength = len(movies_db))

@app.route('/buyTicketAction', methods=["POST"])
def buyAction():
    try:
        filmNumber = int(request.form["movieNumber"])-1
    except:
        return render_template("buy.html", movieList=movies_db, dbLength=len(movies_db), alert=True)
    else:
        if(filmNumber<=0 or filmNumber>=len(movies_db)):
            return render_template("buy.html", movieList=movies_db, dbLength = len(movies_db), alert=True)
        else:
            global currentUser
            movieId = movies_db[filmNumber]
            cinemaSystem.buyTicket(currentUser, movieId)
            return render_template("index.html", userName=currentUser)

@app.route('/cancelTicket')
def cancel():
    global currentUser
    mname = cinemaSystem.tickets[currentUser]
    cinemaSystem.cancelTicket(currentUser)
    return render_template("index.html", userName=currentUser, alert = True, movieName = mname)



# START HERE ------>>>
if __name__ == "__main__":
    app.run(debug=True)
