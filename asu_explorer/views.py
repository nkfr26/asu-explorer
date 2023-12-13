from random import sample
from datetime import datetime, date

from flask import (
    render_template, redirect, url_for, request, jsonify, session
)
from geographiclib.geodesic import Geodesic

from . import app, db, ANS_COORDS
from .models import User
from .form_validation import RegistrationForm


NUM_IMAGES = len(ANS_COORDS)
NUM_QUESTIONS = 3; RADIUS = 25

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    if session.get("questions") is None:
        session.update(
            current_index=0, auth=False,
            questions=sample(range(NUM_IMAGES), NUM_QUESTIONS)
        )

    question = session["questions"][session["current_index"]]
    return render_template(
        "game.html", filename=question,
        NUM_QUESTIONS=NUM_QUESTIONS, currentIndex=session["current_index"]
    )

@app.route("/success", methods=["POST"])
def success():
    question = session["questions"][session["current_index"]]
    distance = Geodesic.WGS84.Inverse(
        *request.json["currentCoords"],
        *ANS_COORDS[question], Geodesic.DISTANCE
    )["s12"]
    is_near_destination = distance <= RADIUS

    if is_near_destination:
        session["auth"] = True

    return jsonify({
        "isNearDestination": is_near_destination  # , "distance": distance
    })

@app.route("/next", methods=["POST"])
def next_():
    if session["auth"]:
        if session["current_index"] != NUM_QUESTIONS - 1:
            session["auth"] = False
            session["current_index"] += 1
        else:
            if session.get("progress") is None:
                session["progress"] = "register"

            del session["questions"]

    return jsonify({
        "hasNextQuestion": bool(session.get("questions"))
    })

@app.route("/reset", methods=["POST"])
def reset():
    del session["questions"]
    return "", 204

@app.route("/game/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    # POSTかつ入力された内容が問題ない場合
    if form.validate_on_submit():
        user = User(
            name=form.name.data,
            date=datetime.now().date(),
            time=datetime.now().time().replace(microsecond=0)
        )
        db.session.add(user)
        db.session.commit()

        session["progress"] = "leaderboard"
        return redirect(url_for("leaderboard"))

    if session.get("progress") == "register":
        return render_template("register.html", form=form)
    else:
        return redirect(url_for("leaderboard"))
    # return render_template("register.html", form=form)

@app.route("/leaderboard")
def leaderboard():
    fest_date = [date(2023, 10, 28), date(2023, 10, 29)]
    filter_by_date = [
        User.query.filter_by(date=fest_date[0]),
        User.query.filter_by(date=fest_date[1])
    ]

    return render_template(
        "leaderboard.html",
        october_28=filter_by_date[0].order_by(User.id.asc()).all(),
        october_29=filter_by_date[1].order_by(User.id.asc()).all(),
        others=User.query.filter(
            User.date.not_in(fest_date)
        ).order_by(User.id.asc()).all()
    )