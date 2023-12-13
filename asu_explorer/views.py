from datetime import datetime, date

from flask import (
    render_template, redirect, url_for, request, make_response
)

from . import app, db, ANS_COORDS
from .models import User
from .form_validation import RegistrationForm


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    return render_template("game.html", ANS_COORDS=ANS_COORDS)

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

        response = make_response(redirect(url_for("leaderboard")))
        response.set_cookie("progress", "leaderboard", 60 * 60 * 24 * 400)
        return response

    if request.cookies.get("progress") == "register":
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