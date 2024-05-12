from flask import Flask, render_template, redirect, request, send_from_directory
import csv
from kafka import KafkaProducer

app = Flask(__name__)

# Initialize Kafka producer
producer = KafkaProducer(bootstrap_servers="localhost:9092")


# Function to read registered users from CSV file
def read_registered_users():
    registered_users = {}
    try:
        with open(
            "/home/anas/Spotify_i22-1987/web_application/logs/registered_users.csv",
            newline="",
        ) as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                registered_users[row[0]] = row[1]
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        pass
    return registered_users


# Function to write registered users to CSV file
def write_registered_users(registered_users):
    with open(
        "/home/anas/Spotify_i22-1987/web_application/logs/registered_users.csv",
        "w",
        newline="",
    ) as csvfile:
        writer = csv.writer(csvfile)
        for username, password in registered_users.items():
            writer.writerow([username, password])


# Route to serve audio files from the static/songs directory
@app.route("/songs/<path:filename>")
def serve_song(filename):
    return send_from_directory("static/songs", filename)


# Route for the login page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        registered_users = read_registered_users()
        if username in registered_users and registered_users[username] == password:
            # Redirect to index page if login successful
            return redirect("/index")
        else:
            # Redirect to register page if login unsuccessful
            return redirect("/register")
    else:
        # Render the login form
        return render_template("login.html")


# Route for the register page
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        registered_users = read_registered_users()
        if username in registered_users:
            # Redirect to login page if user already exists
            return redirect("/login")
        else:
            # Add new user to the CSV file
            registered_users[username] = password
            write_registered_users(registered_users)
            # Redirect to login page after registration
            return redirect("/login")
    else:
        # Render the register form
        return render_template("register.html")


# Route for the index page
@app.route("/")
def start():
    # Redirect to login page
    return redirect("/login")


@app.route("/index")
def index():
    # Render the index page
    return render_template("index.html")


@app.route("/about")
def about():
    # Render the about page
    return render_template("about.html")


@app.route("/show_player/<filename>")
def show_player_page(filename):
    return render_template("player.html", filename=filename)

# Route for the player page
@app.route("/player")
def show_player():
    # Extract song name from request parameters
    song_name = request.args.get("song_name")

    # Send song name to Kafka topic
    producer.send("song_clicks", value=song_name.encode("utf-8"))

    # Render the player page
    return render_template("player.html")


@app.route("/contact")
def contact():
    # Render the contact page
    return render_template("contact.html")


# Route for the playlist page
@app.route("/playlist")
def playlist():
    audios = [
        "140000.mp3",
        "140001.mp3",
        "140002.mp3",
        "140003.mp3",
        "140004.mp3",
        "140005.mp3",
        "140006.mp3",
        "140007.mp3",
        "140008.mp3",
        "140009.mp3",
        "140010.mp3",
        "140079.mp3",
        "140057.mp3",
        "140048.mp3",
        "140012.mp3",
        "140041.mp3",
        "140055.mp3",
        "140039.mp3",
        "140027.mp3",
        "140038.mp3",
        "140022.mp3",
        "140047.mp3",
        "140046.mp3",
        "140044.mp3",
    ]
    return render_template("playlist.html", audios=audios)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
