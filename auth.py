from flask import Blueprint, request, render_template, redirect, session
from models import db, Educator, Parinte

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/")
def index():
    # Afișează pagina de început
    return render_template("index.html")

@auth_bp.route("/login_educator", methods=["GET", "POST"])
def login_educator():
    # Dacă formularul a fost trimis
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # Căutăm educatorul în baza de date
        educator = Educator.query.filter_by(username=user, password=pwd).first()

        if educator:
            # Salvăm educatorul în sesiune
            session["educator_id"] = educator.id
            return redirect("/educator")

        return "Credentiale gresite"

    # Afișăm formularul
    return render_template("login_educator.html")

@auth_bp.route("/login_parinte", methods=["GET", "POST"])
def login_parinte():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        # Căutăm părintele în baza de date
        parinte = Parinte.query.filter_by(username=user, password=pwd).first()

        if parinte:
            session["parinte_id"] = parinte.id
            return redirect("/parinte")

        return "Credentiale gresite"

    return render_template("login_parinte.html")