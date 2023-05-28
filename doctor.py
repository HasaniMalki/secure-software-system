from flask import Blueprint, render_template, redirect, url_for, request, flash
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
# from tensorflow import keras
import joblib
from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User,Role,UserRoles,Donor,Hospital,BloodCampaign,Patient,BloodPacket,BloodTest,BloodIssued,BloodReuestDoctor,BestDonnor,BloodReuestDonnor,BloodRequest,Doctor
from datetime import datetime
from googlegeocoder import GoogleGeocoder

doctor = Blueprint('doctor', __name__)

@doctor.before_request
def before_request():
    if not current_user.is_authenticated :
        flash('Please login first.')
        return redirect(url_for('auth.login'))
    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    if (userrole.name!="doctor"):
        return redirect(url_for('auth.permission'))


@doctor.route('/dashbord/doctor')
def dashbord():
        return render_template('DoctorArea/index.html')

@doctor.route('/dashbord/doctor/patient')
def patient():
        patients=Patient.query.all()
        return render_template('DoctorArea/Patient/index.html',patients=patients)
 
@doctor.route('/dashbord/doctor/patient/add')
def patientAdd():
        return render_template('DoctorArea/Patient/add.html')
        
 
@doctor.route('/dashbord/doctor/patient/add', methods=['POST'])
def patient_post():

    NIC_no = request.form.get('NIC_no')
    name =  request.form.get('name')
    birthday = request.form.get('birthday')
    gender = request.form.get('gender')
    weight =  request.form.get('weight')
    height = request.form.get('height')
    blood_group = request.form.get('blood_group')
    contact_no =  request.form.get('contact_no')

    patient = Patient.query.filter_by(NIC_no=NIC_no).first() 
    
    if patient: 
        flash("NIC no already exists!", 'warning')
        return redirect(url_for('doctor.patientAdd'))
    
    birthday = datetime.strptime(birthday, '%Y-%m-%d')

    new_patient = Patient(
        NIC_no=NIC_no,
        name=name,
        birthday=birthday, 
        gender=gender,
        weight=weight, 
        height=height,
        blood_group=blood_group, 
        contact_no=contact_no,
        Availability="1"
        )
    db.session.add(new_patient)
    db.session.commit()

    flash("Patient added successfully!", 'success')
    return redirect(url_for('doctor.patient'))


        
@doctor.route('/dashbord/doctor/request/<id>')
def requestView(id):
    return render_template('DoctorArea/Patient/requestview.html',id=id)


@doctor.route('/dashbord/doctor/bloodrequest')
def bloodRequest():
        bloodRequests=BloodRequest.query.all()
        return render_template('DoctorArea/bloodRequest/index.html',bloodRequests=bloodRequests)
 
@doctor.route('/dashbord/doctor/bloodrequest/add')
def bloodRequestAdd():
        doctor = Doctor.query.filter_by(email=current_user.email).first()
        bloodRequest = BloodRequest.query.order_by(BloodRequest.id.desc()).first();
        return render_template('DoctorArea/bloodRequest/add.html',doctor=doctor,bloodRequest=bloodRequest)
        
 
@doctor.route('/dashbord/doctor/bloodrequest/add', methods=['POST'])
def blood_request_post():

    nic = request.form.get('nic')
    name =  request.form.get('name')
    age = request.form.get('age')
    reason =  request.form.get('reason')
    height = request.form.get('height')
    bloodtype = request.form.get('bloodtype')
    dID =  request.form.get('dID')
    hospital_id =  request.form.get('hospital_id')
    contract_address =  request.form.get('contract_address')
    tx_hash = request.form.get('tx_hash');
    dname = current_user.name;

    new_bloodRequest = BloodRequest(
        hospital_id=hospital_id,
        pnic=nic,
        pname=name, 
        pphone="65562651",
        age=age, 
        reason=reason, 
        bloodtype=bloodtype,
        dID=dID, 
        dname=dname,
        dinNo="",
        status='false',
        contract_address=contract_address,
        tx_hash=tx_hash,
        )
    db.session.add(new_bloodRequest)
    db.session.commit()

    flash("Blood request added successfully!", 'success')
    return redirect(url_for('doctor.bloodRequest'))


        
@doctor.route('/dashbord/doctor/bloodrequest/<id>')
def bloodrequestView(id):
    bloodRequest = BloodRequest.query.filter_by(id=id).first()
    return render_template('DoctorArea/bloodRequest/requestview.html',bloodRequest=bloodRequest)

