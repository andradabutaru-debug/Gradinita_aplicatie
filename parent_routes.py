from flask import Blueprint, session, render_template, redirect
from models import Parinte, Copil, Meniu, ConsumatieCopil, db
from datetime import date

parent_bp = Blueprint("parinte", __name__)

@parent_bp.route("/parinte")
def parinte_home():
    if "parinte_id" not in session:
        return "Nu esti logat ca parinte"

    parinte = Parinte.query.get(session["parinte_id"])
    copil = Copil.query.get(parinte.copil_id)

    azi = date.today()
    meniu_azi = Meniu.query.filter_by(data=azi).first()

    # consumuri = dict cu meniu_id -> consum
    consumuri = {
        c.meniu_id: c
        for c in ConsumatieCopil.query.filter_by(copil_id=copil.id).all()
    }

    # consumul de azi
    consum_azi = consumuri.get(meniu_azi.id) if meniu_azi else None

    media = None
    if consum_azi:
        media = (
            consum_azi.a_mancat_mic_dejun +
            consum_azi.a_mancat_pranz +
            consum_azi.a_mancat_gustare
        ) / 3
        media = min(media, 100)
        media = round(media)

    return render_template(
        "parent_home.html",
        copil=copil,
        meniu_azi=meniu_azi,
        consum_azi=consum_azi,
        media=media
    )


@parent_bp.route("/marcheaza_absenta", methods=["POST"])
def marcheaza_absenta():
    if "parinte_id" not in session:
        return "Nu esti logat ca parinte"

    parinte = Parinte.query.get(session["parinte_id"])
    copil = Copil.query.get(parinte.copil_id)

    azi = date.today()
    meniu = Meniu.query.filter_by(data=azi).first()

    consum = ConsumatieCopil.query.filter_by(copil_id=copil.id, meniu_id=meniu.id).first()

    if not consum:
        consum = ConsumatieCopil(copil_id=copil.id, meniu_id=meniu.id)
        db.session.add(consum)

    consum.lipseste = True
    db.session.commit()

    return redirect("/parinte")


@parent_bp.route("/logout_parinte")
def logout_parinte():
    session.pop("parinte_id", None)
    return redirect("/")
