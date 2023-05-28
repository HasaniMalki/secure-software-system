from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from . import db
import os
from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User, Role, UserRoles
main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('PublicArea/index.html')

@main.route('/scope')
def scope():
    return render_template('PublicArea/scope.html')

@main.route('/milestones')
def milestones():
    return render_template('PublicArea/milestones.html')

@main.route('/documents')
def documents():
    return render_template('PublicArea/documents.html')

@main.route('/presentations')
def presentations():
    return render_template('PublicArea/presentations.html')

@main.route('/dashbord')
def dashbord():
    
    if not current_user.is_authenticated :
        flash('Please login first.')
        return redirect(url_for('auth.login'))

    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    if (userrole.name=="admin"):
        return redirect(url_for('admin.dashbord'))
        
    elif (userrole.name=="doctor"):
        return redirect(url_for('doctor.dashbord'))
        
    elif (userrole.name=="manager"):
        return redirect(url_for('manager.dashbord'))

    elif (userrole.name=="donor"):
        return redirect(url_for('donors.dashbord'))
    else:
        flash('You are not admin')
        return redirect(url_for('auth.login'))
        