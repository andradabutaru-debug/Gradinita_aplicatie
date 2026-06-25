from app import create_app
from models import db, Educator, Copil, Parinte, Meniu
from datetime import date, timedelta

app = create_app()

with app.app_context():

    db.drop_all()
    db.create_all()

    # Educatori
    for i in range(1, 6):
        db.session.add(Educator(username=f"educator{i}", password="parola123"))

    db.session.commit()

    # Copii + Parinti
    copii = []
    for i in range(1, 26):
        copil = Copil(nume=f"Copil_{i}")
        db.session.add(copil)
        copii.append(copil)

    db.session.commit()

    for i, copil in enumerate(copii, start=1):
        db.session.add(Parinte(username=f"parinte{i}", password="parola123", copil_id=copil.id))

    db.session.commit()

    # Meniu 7 zile
    azi = date.today()
    for i in range(7):
        zi = azi + timedelta(days=i)
        db.session.add(Meniu(
            data=zi,
            mic_dejun=f"Mic dejun {i+1}",
            pranz=f"Pranz {i+1}",
            gustare=f"Gustare {i+1}"
        ))

    db.session.commit()

    print("Populare completa!")
