from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tools.eval_measures import rmse
from sklearn.preprocessing import MinMaxScaler
from keras.preprocessing.sequence import TimeseriesGenerator
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
from keras.layers import Dropout
import warnings
from tensorflow import keras
import joblib
from flask import Flask, render_template, Blueprint, redirect, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User, Role, UserRoles, Donor, Hospital, BloodCampaign, Patient, BloodPacket, BloodTest, BloodIssued, BloodReuestDoctor, BestDonnor, BloodReuestDonnor, BloodRequest, BloodDonnerRequestNow
from datetime import datetime
from googlegeocoder import GoogleGeocoder
import csv
import json
import project.datasetview as datasetview
from pandas.tseries.offsets import DateOffset
import math
from twilio.rest import Client
import flask
from flask import request as flaskreq
donors = Blueprint('donors', __name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@donors.before_request
def before_request():
    if not current_user.is_authenticated:
        flash('Please login first.')
        return redirect(url_for('auth.login'))
    userroles = UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole = Role.query.filter_by(id=userroles.role_id).first()
    # if (userrole.name != "donor"):
    #     return redirect(url_for('auth.permission'))


@donors.route('/dashbord/donors')
def dashbord():
    return render_template('DonorArea/index.html')


@donors.route('/dashbord/donors/request')
def request():
    donordata = Donor.query.filter_by(NIC_no=current_user.NIC_no).first()
    donordatas = BloodReuestDonnor.query.filter_by(
        donnor_id=donordata.id).all()
    return render_template('DonorArea/Request/index.html', donordatas=donordatas)


@donors.route('/dashbord/donors/request/<id>')
def requestView(id):
    bloodRequest = BloodDonnerRequestNow.query.filter_by(id=id).first()
    return render_template('DonorArea/Request/view.html', id=id, bloodRequest=bloodRequest)


@donors.route('/dashbord/donors/request/update', methods=['POST'])
def requestUpdateNow():

    idValue = flaskreq.form.get('idValue')
    inlineRadioOptions = flaskreq.form.get('inlineRadioOptions')
    inlineRadioOptions1 = flaskreq.form.get('inlineRadioOptions1')
    weight = flaskreq.form.get('weight')
    time = flaskreq.form.get('time')
    status = 'false'
    if inlineRadioOptions == 'option1':
        status = 'not'
    else:
        status = 'true'

    bloodRequest = BloodDonnerRequestNow.query.filter_by(id=idValue).first()

    bloodRequest.status = status
    bloodRequest.disease = inlineRadioOptions1
    bloodRequest.weight = weight
    bloodRequest.time = time

    db.session.commit()

    flash("Blood request updated successfully!", 'success')
    return redirect(url_for('donors.dashbord'))
