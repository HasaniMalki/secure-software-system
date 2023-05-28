from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User, Role, UserRoles
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        flash('You login')
        return redirect(url_for('main.index'))

    return render_template('PublicArea/login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('main.dashbord'))

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    
    if user: # if a user is found, we want to redirect back to signup page so user can try again
        flash('Email address already exists.')
        return redirect(url_for('auth.signup'))

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    role1 =Role.query.filter_by(name='admin').first()
    # role1 = Role(name='developerff')
    new_user.roles.append(role1)
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
def logout():
    logout_user()
    flash('You are logout successfully.')
    return redirect(url_for('main.index'))
    
@auth.route('/permission')
def permission():
    if not current_user.is_authenticated :
        return redirect(url_for('main.index'))
    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    return render_template('PublicArea/permission.html',userrole=userrole.name)
