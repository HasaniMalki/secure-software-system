from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User, Role, UserRoles
technician = Blueprint('technician', __name__)

@technician.before_request
def before_request():
    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    if not current_user.is_authenticated :
        flash('Please login first.')
        return redirect(url_for('auth.login'))
    if (userrole.name!="manager"):
        return redirect(url_for('auth.permission'))


@technician.route('/dashbord/manager')
def dashbord():
        return render_template('ManagerArea/index.html')

@technician.route('/dashbord/manager/donor')
def donor():
        return render_template('ManagerArea/Donor/index.html')

@technician.route('/dashbord/manager/blooddemand')
def blooddemand():
        return render_template('ManagerArea/Blooddemand/index.html')

@technician.route('/dashbord/manager/bloodcamp')
def bloodcamp():
        return render_template('ManagerArea/BloodCamp/index.html')

