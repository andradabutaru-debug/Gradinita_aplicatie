from flask import Blueprint, session, render_template, redirect
from models import Parinte, Copil, Meniu, ConsumatieCopil, db
from datetime import datetime, date

parent_bp = Blueprint("parinte", __name__)

@parent_bp.route("/parinte")
def parinte_home():
    # Verificăm dacă părintele este logat
    if "parinte_id" not in session:
        return "Nu esti logat ca parinte"

    # Luăm părintele logat
    parinte = Parinte.query.get(session["parinte_id"])

    # Luăm copilul asociat părintelui
    copil = Copil.query.get(parinte.copil_id)

    from datetime import date

    azi = date.today()

    # Luăm DOAR meniul de azi
    meniu_azi = Meniu.query.filter_by(data=azi).first()

    # Luăm consumul copilului
    consumuri = {
        c.meniu_id: c
        for c in ConsumatieCopil.query.filter_by(copil_id=copil.id).all()
    }

    # Trimitem datele către template-ul corect
    return render_template(
        "parent_home.html",
        copil=copil,
        meniu_azi=meniu_azi,
        consumuri=consumuri
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
