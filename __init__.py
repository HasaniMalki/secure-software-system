from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_toastr import Toastr

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'secret-key-goes-here'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
    toastr = Toastr(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import Role
    from .models import User
    from .models import UserRoles
    from .models import Donor
    from .models import BloodCampaign
    from .models import Hospital
    from .models import Patient
    from .models import BloodPacket
    from .models import BloodTest
    from .models import BloodIssued
    from .models import BloodReuestDoctor
    from .models import BloodReuestDonnor
    from .models import BestDonnor
    
    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))
        
    db.init_app(app)
    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for admin parts of app
    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    # blueprint for doctor parts of app
    from .doctor import doctor as doctor_blueprint
    app.register_blueprint(doctor_blueprint)

    # blueprint for manager parts of app
    from .manager import manager as manager_blueprint
    app.register_blueprint(manager_blueprint)

    # blueprint for technician parts of app
    from .technician import technician as technician_blueprint
    app.register_blueprint(technician_blueprint)

    # blueprint for donor parts of app
    from .donors import donors as donor_blueprint
    app.register_blueprint(donor_blueprint)

    return app
