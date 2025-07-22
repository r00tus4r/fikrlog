from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect
from datetime import datetime

import os
import dotenv
dotenv.load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static', static_url_path='/')
    app.secret_key = os.getenv('SECRET_KEY', 'dev-fallback-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fikrlog.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ADMIN_USERNAME'] = os.getenv('ADMIN_USERNAME')
    app.config['ADMIN_PASSWORD_HASH'] = os.getenv('ADMIN_PASSWORD_HASH')

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)

    login_manager.login_message = 'Ushbu sahifani ko‘rish uchun tizimga kiring!'
    login_manager.login_message_category = 'info'
    login_manager.login_view = 'auth.login'

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('403.html'), 403

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow}


    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from . import routes, auth
    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp, url_prefix='/auth')

    with app.app_context():
        db.create_all()
        admin = User.query.filter_by(username=app.config['ADMIN_USERNAME']).first()
        if not admin:
            new_admin = User(username=app.config['ADMIN_USERNAME'], password=app.config['ADMIN_PASSWORD_HASH'])
            db.session.add(new_admin)
            db.session.commit()
            print(" * Admin user created.")
        else:
            print(" * Admin user already exists.")
        print(f" * Database connected: {app.config['SQLALCHEMY_DATABASE_URI']}")

    return app
