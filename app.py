from flask import Flask
from models import db
from auth import auth_bp
from educator_routes import educator_bp
from parent_routes import parent_bp

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'cheie_secreta'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gradinita.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(educator_bp)
    app.register_blueprint(parent_bp)

    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
