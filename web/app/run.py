from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime, timedelta, timezone
app = Flask(__name__)
app.secret_key = "development-secret-key"

GOSSIP_GRANTS = {}

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
    errors = {}
    form_data = {"role": "Knight", "strength": 10, "dexterity": 10, "constitution": 10}
    
    if request.method == "POST":
        form_data = request.form.to_dict()
        role = form_data.get("role", "Knight")
        login = form_data.get("login", "").strip()
        password = form_data.get("password", "")
        selected_house = form_data.get("house", "")

        if role not in {"Knight", "Lord", "Smallfolk"}:
            errors["role"] = "Please choose a role."
        if not login:
            errors["login"] = "Please enter your name."
        elif login in USERS:
            errors["login"] = "That name is already taken."

        if len(password) < 8:
            errors["password"] = "Use at least 8 characters with numbers."

        house = next((h for h in HOUSES if h["name"] == selected_house), None)
        if not house:
            errors["house"] = "Please choose your house."

    
        if not errors:
            USERS[login] = {
                "id": len(USERS) + 1,
                "name": login,
                "password": password,
                "role": role,
                "house": house["name"] if house else None,
                "strength": int(form_data.get("strength", 10)) if role == "Knight" else None,
                "dexterity": int(form_data.get("dexterity", 10)) if role == "Knight" else None,
                "constitution": int(form_data.get("constitution", 10)) if role == "Knight" else None,
                "image_url": "",
            }
            print(USERS[login])
            return redirect(url_for("login"))

    return render_template(
        "register.html",
        houses=HOUSES,
        errors=errors,
        form_data=form_data)

@app.route("/logout")
def logout():
    return redirect(url_for("login"))

@app.route("/book-of-knights")
def book_of_knights():
    return render_template("base.html")

if (__name__ == "__main__") :
    app.run(host="0.0.0.0", port=5000)
