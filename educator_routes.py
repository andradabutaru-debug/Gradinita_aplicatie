from flask import Blueprint, session, render_template, redirect, request
from models import Parinte, Copil, Meniu, ConsumatieCopil, db
from datetime import date

educator_bp = Blueprint("educator", __name__)


# ------------------------------
# PAGINA PRINCIPALĂ EDUCATOR
# ------------------------------
@educator_bp.route("/educator")
def educator_home():
    if "educator_id" not in session:
        return redirect("/login_educator")

    copii = Copil.query.all()

    azi = date.today()
    meniu_azi = Meniu.query.filter_by(data=azi).first()

    # Construim dictionarul consumuri
    consumuri = {}

    if meniu_azi:
        for copil in copii:
            consum = ConsumatieCopil.query.filter_by(
                copil_id=copil.id,
                meniu_id=meniu_azi.id
            ).first()
            consumuri[copil.id] = consum
    else:
        for copil in copii:
            consumuri[copil.id] = None

    return render_template(
        "educator_home.html",
        copii=copii,
        meniu_azi=meniu_azi,
        consumuri=consumuri
    )


# ------------------------------
# UPDATE MENIU ZIUA CURENTĂ
# ------------------------------
@educator_bp.route("/update_meniu_azi", methods=["POST"])
def update_meniu_azi():
    if "educator_id" not in session:
        return redirect("/login_educator")

    azi = date.today()
    meniu = Meniu.query.filter_by(data=azi).first()

    if meniu:
        meniu.mic_dejun = request.form["mic_dejun"]
        meniu.pranz = request.form["pranz"]
        meniu.gustare = request.form["gustare"]
        db.session.commit()

    return redirect("/educator")


# ------------------------------
# DETALII COPIL
# ------------------------------
@educator_bp.route("/copil/<int:copil_id>")
def copil_detalii(copil_id):
    if "educator_id" not in session:
        return redirect("/login_educator")

    copil = Copil.query.get(copil_id)

    azi = date.today()
    meniu_azi = Meniu.query.filter_by(data=azi).first()

    consum = None
    if meniu_azi:
        consum = ConsumatieCopil.query.filter_by(
            copil_id=copil.id,
            meniu_id=meniu_azi.id
        ).first()

    return render_template(
        "copil_detalii.html",
        copil=copil,
        meniu_azi=meniu_azi,
        consum=consum
    )


# ------------------------------
# UPDATE CONSUM COPIL (PROCENTE)
# ------------------------------
@educator_bp.route("/update_consum/<int:copil_id>", methods=["POST"])
def update_consum(copil_id):
    if "educator_id" not in session:
        return redirect("/login_educator")

    copil = Copil.query.get(copil_id)
    azi = date.today()
    meniu = Meniu.query.filter_by(data=azi).first()

    if not meniu:
        return redirect(f"/copil/{copil.id}")

    consum = ConsumatieCopil.query.filter_by(
        copil_id=copil.id,
        meniu_id=meniu.id
    ).first()

    if not consum:
        consum = ConsumatieCopil(
            copil_id=copil.id,
            meniu_id=meniu.id
        )
        db.session.add(consum)

    if consum.lipseste:
        return redirect(f"/copil/{copil.id}")

    # Salvăm procentele
    consum.a_mancat_mic_dejun = int(request.form.get("mic_dejun", 0))
    consum.a_mancat_pranz = int(request.form.get("pranz", 0))
    consum.a_mancat_gustare = int(request.form.get("gustare", 0))

    db.session.commit()

    return redirect(f"/copil/{copil.id}")


# ------------------------------
# LOGOUT EDUCATOR
# ------------------------------
@educator_bp.route("/logout_educator")
def logout_educator():
    session.pop("educator_id", None)
    return redirect("/")
