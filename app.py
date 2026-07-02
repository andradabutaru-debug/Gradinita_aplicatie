from flask import Flask, redirect, session, render_template
from models import db
from auth import auth_bp
from educator_routes import educator_bp
from parent_routes import parent_bp

app = Flask(__name__)
app.secret_key = "secretul_tau_aici"

# Configurare baza de date
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///gradinita.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Înregistrăm blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(educator_bp)
app.register_blueprint(parent_bp)


# ---------------------------------------------------
# PAGINA DE ACASĂ — REDIRECT CORESPUNZĂTOR USERULUI
# ---------------------------------------------------
@app.route("/")
def home():
    # Dacă educatorul este logat → panou educator
    if "educator_id" in session:
        return redirect("/educator")

    # Dacă părintele este logat → panou părinte
    if "parinte_id" in session:
        return redirect("/parinte")

    # Dacă nimeni nu este logat → pagina neutră de login
    return redirect("/login")


# ---------------------------------------------------
# PAGINA DE LOGIN NEUTRĂ
# ---------------------------------------------------
@app.route("/login")
def login_page():
    return render_template("login.html")


# ---------------------------------------------------
# PORNIRE APLICAȚIE
# ---------------------------------------------------
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
