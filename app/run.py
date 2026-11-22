from flask import Flask, redirect, render_template, request, session, url_for
from datetime import datetime, timedelta, timezone

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
        "role": "Knight",
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
    "role": "Knight",
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
    "role": "Lord",
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
    "role": "Knight",
    "house": "House Hightower",
    "strength": 13,
    "dexterity": 14,
    "constitution": 16,
    "image_url": "",
},
}

GOSSIP_GRANTS = {}

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

@app.route("/register", methods=["GET", "POST"])
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
            print(USERS)
            return redirect(url_for("login"))

    return render_template(
        "register.html",
        houses=HOUSES,
        errors=errors,
        form_data=form_data)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# @app.route("/book-of-knights")
# def book_of_knights():
#     active_role = request.args.get("role", "all")
#     active_house = request.args.get("house", "all")

#     entries = [u for u in USERS.values() if u["role"] in {"knight", "lord"}]
#     if active_role in {"knight", "lord"}:
#         entries = [e for e in entries if e["role"] == active_role]
#     if active_house != "all":
#         entries = [e for e in entries if e["house"] == active_house]

#     retrieved_password = session.pop("retrieved_gossip_password", None)

#     now = datetime.now(timezone.utc)
#     requester_id = session.get("user_id")

#     gossip_access_ids = {
#         target_id
#         for (user_id, target_id), grant in GOSSIP_GRANTS.items()
#         if user_id == requester_id
#         and grant["expires_at"] > now
#     }
 
#     print("user logged in = ", session['user']['login'])
#     print(USERS.get(session['user']['login']))
#     print(USERS)
#     return render_template(
#         "book_of_knights.html",
#         entries=entries,
#         houses=HOUSES,
#         active_role=active_role,
#         active_house=active_house,
#         # gossip_used_today=bool(session.get("gossip_used_today")),
#         current_user=USERS.get(session['user']['login']),
#         retrieved_gossip_password=retrieved_password,
#         gossip_access_ids=gossip_access_ids,
#         gossip_used_today=(session.get("gossip_used_date") == datetime.now(timezone.utc).date().isoformat())
#     )


@app.route("/book-of-knights")
def book_of_knights():
    active_role = request.args.get("role", "all")
    active_house = request.args.get("house", "all")

    entries = [u for u in USERS.values() if u["role"] in {"Knight", "Lord"}]
    if active_role in {"Knight", "Lord"}:
        entries = [e for e in entries if e["role"] == active_role]
    if active_house != "all":
        entries = [e for e in entries if e["house"] == active_house]

    retrieved_password = session.pop("retrieved_gossip_password", None)

    now = datetime.now(timezone.utc)
    requester_id = session.get("user_id")

    gossip_access_ids = {
        target_id
        for (user_id, target_id), grant in GOSSIP_GRANTS.items()
        if user_id == requester_id
        and grant["expires_at"] > now
    }

    print(USERS)

    return render_template(
        "book_of_knights.html",
        entries=entries,
        houses=HOUSES,
        active_role=active_role,
        active_house=active_house,
        # gossip_used_today=bool(session.get("gossip_used_today")),
        current_user=USERS.get(session['user']['login']),
        retrieved_gossip_password=retrieved_password,
        gossip_access_ids=gossip_access_ids,
        gossip_used_today=(session.get("gossip_used_date") == datetime.now(timezone.utc).date().isoformat())
    )


@app.route("/gossip/<int:knight_id>", methods=["POST"])
def post_gossip(knight_id):
    entered_password = request.form.get("gossip_password", "")

    requester_id = session.get("user_id")

    requester = next(
        (user for user in USERS.values()
         if user["id"] == requester_id),
        None
    )

    target = next(
        (user for user in USERS.values()
         if user["id"] == knight_id),
        None
    )

    today = datetime.now(timezone.utc).date().isoformat()

    if session.get("gossip_used_date") == today:
        return redirect(url_for("book_of_knights"))
  
    # Validate target's Gossip password
    if not (target["gossip_password"] == entered_password):
        print(f"Entered password: {entered_password}, Target's gossip password hash: {target['gossip_password']}")
        # flash("Incorrect Gossip password.", "error")
        return redirect(url_for("book_of_knights"))

    # Create a 24-hour access grant
    now = datetime.now(timezone.utc)

    GOSSIP_GRANTS[(requester_id, knight_id)] = {
        "granted_at": now,
        "expires_at": now + timedelta(hours=24)
    }

    # Consume daily allowance
    session["gossip_used_date"] = today

    # flash(
    #     f"You can now view {target['name']}'s restricted statistics for 24 hours.",
    #     "success"
    # )

    return redirect(url_for("book_of_knights"))


@app.route("/gossip", methods=["GET"]) 
def get_knight_gossip_password():
    if session.get("gossip_used_today"):
        # flash("You have already used your daily Gossip.", "error")
        return redirect(url_for("book_of_knights"))

    knight_id = request.args.get("knight_id", type=int)

    knight = next((user for user in USERS.values() if user["id"] == knight_id),None)
    if knight:
        session["retrieved_gossip_password"] = knight.get("gossip_password")
    return redirect(url_for("book_of_knights"))


if __name__ == "__main__":
    app.run(debug=True)