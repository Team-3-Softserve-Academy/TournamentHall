from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "development-secret-key"


HOUSES = [
    {"name": "House Vance"},
    {"name": "House Corbray"},
    {"name": "House Hightower"},
    {"name": "House Tarly"},
    {"name": "House Blackwood"},
]
 
USERS = {
    "Ser Aldric Vance": {
        "id": 1,
        "name": "Ser Aldric Vance",
        "password": "tourney123",
        "role": "knight",
        "house": "House Vance",
        "strength": 14,
        "dexterity": 12,
        "constitution": 13,
        "image_url": "",
    },
 
   "Ser Edmund Blackwood": {
    "id": 2,
    "name": "Ser Edmund Blackwood",
    "password": "blackwood123",
    "role": "knight",
    "house": "House Blackwood",
    "strength": 16,
    "dexterity": 11,
    "constitution": 14,
    "image_url": "",
},

"Lord Brynden Blackwood": {
    "id": 3,
    "name": "Lord Brynden Blackwood",
    "password": "blacklord123",
    "role": "lord",
    "house": "House Blackwood",
    "strength": 15,
    "dexterity": 12,
    "constitution": 16,
    "image_url": "",
},

"Ser Gareth Hightower": {
    "id": 4,
    "name": "Ser Gareth Hightower",
    "password": "hightower123",
    "role": "knight",
    "house": "House Hightower",
    "strength": 13,
    "dexterity": 14,
    "constitution": 16,
    "image_url": "",
},
}

@app.route("/login", methods=["GET", "POST"])
def login():
    errors = {}
    form_data = {} 
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        login = form_data.get("login", "").strip()
        password = form_data.get("password", "")

        if not login:
            errors["login"] = "Please enter your login."
        if not password:
            errors["password"] = "Please enter your password."

        if not errors:
            session["user"] = {"login": login}
            return redirect(url_for("book_of_knights"))
            

    return render_template(
        "login.html",
        errors=errors,
        form_data=form_data,
    )

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/book-of-knights")
def book_of_knights():
    return render_template("base.html")

@app.route("/register")
def register():
    return render_template("base.html")

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)