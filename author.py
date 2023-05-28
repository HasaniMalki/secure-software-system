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
from tensorflow import keras
import joblib
from flask import Flask, render_template, request, Blueprint, redirect, url_for, flash
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_user import login_required, SQLAlchemyAdapter, UserManager, UserMixin, current_user, roles_required
from .models import User,Role,UserRoles,Donor,Hospital,BloodCampaign,Patient,BloodPacket,BloodTest,BloodIssued,BloodReuestDoctor,BestDonnor,BloodReuestDonnor,BloodRequest,BloodDonnerRequestNow
from datetime import datetime
from googlegeocoder import GoogleGeocoder
import csv
import json
import project.datasetview as datasetview
from pandas.tseries.offsets import DateOffset
import math
from twilio.rest import Client
import flask

author = Blueprint('author', __name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
@manager.before_request
def before_request():
    if not current_user.is_authenticated :
        flash('Please login first.')
        return redirect(url_for('auth.login'))

    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    if (userrole.name!="manager"):
        return redirect(url_for('auth.permission'))

@manager.route('/dashbord/manager/donor/best')
def bestDonor():
        BloodReuests=BloodDonnerRequestNow.query.all()
        return render_template('ManagerArea/Donor/bestIndex.html',BloodRetests=BloodRetests)

# Role route
@manager.route('/dashbord/manager/donor/best/<int:id>/view', methods=['GET'])
def bestDonorView(id):
        BloodRequest = BloodDonnerRequestNow.query.filter_by(id=id).first()
        return render_template('ManagerArea/Donor/bestView.html',BloodRequest=BloodRequest)
###################################################################
@manager.route('/dashbord/manager/donor/best/new')
def bestDonorAdd():

        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        AllCount=0
        ACount=0
        BCount=0
        OCount=0
        ABCount=0
        NCount=0
        with open(ROOT_DIR+'/data/Hospitals.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                first_line = True
                data_list = []
                for row in data:
                        if not first_line:
                                data_list.append({
                                "SerialNo": row[0],
                                "name": row[1],
                                "Longitude": row[2],
                                "Latitude": row[3]
                                })
                                
                        else:
                                first_line = False
        hospitals=Hospital.query.all()
        donor_lists=datasetview.donor

        donor_lists = donor_lists.reset_index().values.tolist()

        for donor_list in donor_lists:
                AllCount=AllCount+1
                if (donor_list[16]=="A+"):
                        ACount=ACount+1
                elif(donor_list[16]=="B+"):
                        BCount=BCount+1
                elif(donor_list[16]=="O+"):
                        OCount=OCount+1
                elif(donor_list[16]=="AB+"):
                        ABCount=ABCount+1
                else:
                        NCount=NCount+1

        count_list = [(AllCount),(ACount),(BCount),(OCount),(ABCount),(NCount)]     
        return render_template('ManagerArea/Donor/bestAdd.html',hospitals=data_list,count_list=count_list)


@manager.route('/dashbord/manager/donor/best/new', methods=['POST'])
def bestDonor_post():
        hospital_id = request.form.get('hospital_id')
        blood_group = request.form.get('blood_group')
        stage = request.form.get('stage')
        number_of_donnors = request.form.get('number_of_donnors')
        reason = request.form.get('reason')
        
        with open(ROOT_DIR+'/data/Hospitals.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                first_line = True
                data_list = []
                for row in data:
                        if not first_line:
                                if  (row[0]==hospital_id):
                                        data_list_latitude=row[2]
                                        data_list_longitude=row[3]
                                        data_list.append({
                                        "SerialNo": row[0],
                                        "name": row[1],
                                        "Longitude": row[2],
                                        "Latitude": row[3]
                                        })
                                
                        else:
                                first_line = False

        latitude = float(data_list_longitude)
        longitude = float(data_list_latitude)

        stage = int(request.form.get('stage'))
        Blood_Group = str(request.form.get('blood_group'))
        count = int(request.form.get('number_of_donnors'))


        maxlatitude = maxlat(latitude, stage)
        minlatitude = minlat(latitude, stage)
        maxlongitude = maxlon(longitude, stage)
        minlongitude = minlon(longitude, stage)


        # ////////////////////////////////////////////////////////////// Selecting suitable donors according to the stages

        DONORRESULT_BloodType=datasetview.DONORRESULT_BloodType
        Available_DONORRESULT_BloodType=datasetview.Available_DONORRESULT_BloodType
        Distance_KM=datasetview.Distance_KM

        DONORRESULT_BloodType = bestDonor(Blood_Group,minlatitude,maxlatitude,minlongitude,maxlongitude)
       

        DONORRESULT_BloodType = DONORRESULT_BloodType.reset_index()



        # ////////////////////////////////////////////////////////////////////////// Check availability, age and next blood donation date
        Available_DONORRESULT_BloodType = datasetview.Available_DONORRESULT_BloodType
        Available_DONORRESULT_BloodType = Available_DONORRESULT_BloodType.iloc[0:0]


        for i in range(len(DONORRESULT_BloodType)):
                today = datetime.today()
                nextbloodDOnationDate = pd.to_datetime(DONORRESULT_BloodType.Date_of_Next_Blood_Donation[i])
                if (DONORRESULT_BloodType.Age[i] <= 60 and DONORRESULT_BloodType.Availability[i] == 'Available' and nextbloodDOnationDate < today):
                        Available_DONORRESULT_BloodType.loc[i] = [DONORRESULT_BloodType.Serial_No[i]] + [
                        DONORRESULT_BloodType.Latitude[i]] + [DONORRESULT_BloodType.Longitude[i]] + [DONORRESULT_BloodType.Contact_No[i]]


        # Available_DONORRESULT_BloodType = data.Available_DONORRESULT_BloodType.reset_index()
        Available_DONORRESULT_BloodType = Available_DONORRESULT_BloodType.reset_index()

        # /////////////////////////////////////////////////////////////////// Mathematical process

        Distance_KM = datasetview.Distance_KM
        Distance_KM = Distance_KM.iloc[0:0]
        for j in range(len(Available_DONORRESULT_BloodType)):

                p1 = [latitude, longitude]
                p2 = [Available_DONORRESULT_BloodType.Latitude[j], Available_DONORRESULT_BloodType.Longitude[j]]

                R = 6373.0
                lat1 = math.radians(p1[0])
                lon1 = math.radians(p1[1])
                lat2 = math.radians(p2[0])
                lon2 = math.radians(p2[1])

                dlon = lon2 - lon1
                dlat = lat2 - lat1

                a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
                c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
                distance = R * c
                Distance_KM.loc[j] = [Available_DONORRESULT_BloodType.Serial_No[j]] + [distance] + [
                Available_DONORRESULT_BloodType.Contact_No[j]]



        Final_list = Distance_KM.sort_values(by=['Distance']).reset_index().head(count)
        Final = Final_list.reset_index().values.tolist()
        data_list = []
        first_line = True
        idVlaue = 0
        for Finals in Final:
                donorname=""
                with open(ROOT_DIR+'/data/Donors.csv') as csv_file:
                        datawe = csv.reader(csv_file, delimiter=',')
                        for row in datawe:
                                if not first_line:
                                        if  (row[0]==Finals[2]):
                                                donorname= row[1]
                                else:
                                        first_line = False
                idVlaue=idVlaue+1
                data_list.append({
                "id": idVlaue,
                "SerialNo": Finals[2],
                "Name": donorname,
                "Distance": Finals[3],
                "Contact": Finals[4]
                })

                new_bloodRequest = BloodDonnerRequestNow(
                        s_number= Finals[2],
                        name=donorname,
                        distance=Finals[3],
                        status='false',
                        contact= Finals[4],
                        )
                db.session.add(new_bloodRequest)
                db.session.commit()
        newBloodReuests = data_list;
        return render_template('ManagerArea/Donor/Addnew.html',BloodReuests=data_list)

@manager.route('/dashbord/manager/bloodpacket/assign')
def bloodpacket_post():
        return render_template('ManagerArea/BloodPacket/requestview.html',)


def LoadPastDataset(bloodgrop):

        df = pd.read_csv(ROOT_DIR+'/datamodel/all.csv')

        if bloodgrop=="All":
                df =  df.drop(['O+','O-','B+','B-','A+','A-','AB+','AB-'], axis=1)
        elif bloodgrop=="A+":
                df =  df.drop(['O+','O-','B+','B-','All','A-','AB+','AB-'], axis=1)
        elif bloodgrop=="A-":
                df =  df.drop(['O+','O-','B+','B-','All','A+','AB+','AB-'], axis=1)
        elif bloodgrop=="B+":
                df =  df.drop(['O+','O-','A-','B-','All','A+','AB+','AB-'], axis=1)
        elif bloodgrop=="B-":
                df =  df.drop(['O+','O-','B+','A-','All','A+','AB+','AB-'], axis=1)
        elif bloodgrop=="O+":
                df =  df.drop(['A-','O-','B+','B-','All','A+','AB+','AB-'], axis=1)
        elif bloodgrop=="O-":
                df =  df.drop(['O+','A-','B+','B-','All','A+','AB+','AB-'], axis=1)
        elif bloodgrop=="AB-":
                df =  df.drop(['O+','A-','B+','B-','All','A+','AB+','O-'], axis=1)
        elif bloodgrop=="AB+":
                df =  df.drop(['O+','A-','B+','B-','All','A+','O-','AB-'], axis=1)
        df.Date = pd.to_datetime(df.Date)
        df = df.set_index('Date')

        return df



def maxlat(currentvalue, stage_No):

    if (stage_No == 1):
        return currentvalue + 0.01
    elif (stage_No == 2):
        return currentvalue + 0.05
    elif (stage_No == 3):
        return currentvalue + 0.1


def minlat(currentvalue, stage_No):
    if (stage_No == 1):
        return currentvalue - 0.01
    elif (stage_No == 2):
        return currentvalue - 0.05
    elif (stage_No == 3):
        return currentvalue - 0.1


def maxlon(currentvalue, stage_No):
    if (stage_No == 1):
        return currentvalue + 0.1
    elif (stage_No == 2):
        return currentvalue + 0.3
    elif (stage_No == 3):
        return currentvalue + 0.5


def minlon(currentvalue, stage_No):
    if (stage_No == 1):
        return currentvalue - 0.1
    elif (stage_No == 2):
        return currentvalue - 0.3
    elif (stage_No == 3):
        return currentvalue - 0.5


def bestDonor(Blood_Group,minlatitude,maxlatitude,minlongitude,maxlongitude):
    
    DONORRESULT_BloodType = datasetview.DONORRESULT_BloodType
    DONORRESULT_BloodType = DONORRESULT_BloodType.iloc[0:0]

    if (Blood_Group == "ABN"):
        for i in range(len(datasetview.ABN_result)):
            if (minlatitude <= datasetview.ABN_result.Latitude[i] and maxlatitude >= datasetview.ABN_result.Latitude[i]) and (
                    minlongitude <= datasetview.ABN_result.Longitude[i] and maxlongitude >= datasetview.ABN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.ABN_result.Serial_No[i]] + [datasetview.ABN_result.Latitude[i]] + [
                    datasetview.ABN_result.Longitude[i]] + [datasetview.ABN_result.Contact_No[i]] + [datasetview.ABN_result.Age[i]] + [
                                                        datasetview.ABN_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.ABN_result.Availability[i]]

    elif (Blood_Group == "AP"):
        for i in range(len(datasetview.AP_result)):
            if (minlatitude <= datasetview.AP_result.Latitude[i] and maxlatitude >= datasetview.AP_result.Latitude[i]) and (
                    minlongitude <= datasetview.AP_result.Longitude[i] and maxlongitude >= datasetview.AP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.AP_result.Serial_No[i]] + [datasetview.AP_result.Latitude[i]] + [
                    datasetview.AP_result.Longitude[i]] + [datasetview.AP_result.Contact_No[i]] + [datasetview.AP_result.Age[i]] + [
                                                        datasetview.AP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.AP_result.Availability[i]]

    elif (Blood_Group == "BP"):
        for i in range(len(datasetview.BP_result)):
            if (minlatitude <= datasetview.BP_result.Latitude[i] and maxlatitude >= datasetview.BP_result.Latitude[i]) and (
                    minlongitude <= datasetview.BP_result.Longitude[i] and maxlongitude >= datasetview.BP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.BP_result.Serial_No[i]] + [datasetview.BP_result.Latitude[i]] + [
                    datasetview.BP_result.Longitude[i]] + [datasetview.BP_result.Contact_No[i]] + [datasetview.BP_result.Age[i]] + [
                                                        datasetview.BP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.BP_result.Availability[i]]

    elif (Blood_Group == "ABP"):
        for i in range(len(datasetview.ABP_result)):
            if (minlatitude <= datasetview.ABP_result.Latitude[i] and maxlatitude >= datasetview.ABP_result.Latitude[i]) and (
                    minlongitude <= datasetview.ABP_result.Longitude[i] and maxlongitude >= datasetview.ABP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.ABP_result.Serial_No[i]] + [datasetview.ABP_result.Latitude[i]] + [
                    datasetview.ABP_result.Longitude[i]] + [datasetview.ABP_result.Contact_No[i]] + [datasetview.ABP_result.Age[i]] + [
                                                        datasetview.ABP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.ABP_result.Availability[i]]


    elif (Blood_Group == "AN"):
        for i in range(len(datasetview.AN_result)):
            if (minlatitude <= datasetview.AN_result.Latitude[i] and maxlatitude >= datasetview.AN_result.Latitude[i]) and (
                    minlongitude <= datasetview.AN_result.Longitude[i] and maxlongitude >= datasetview.AN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.AN_result.Serial_No[i]] + [datasetview.AN_result.Latitude[i]] + [
                    datasetview.AN_result.Longitude[i]] + [datasetview.AN_result.Contact_No[i]] + [datasetview.AN_result.Age[i]] + [
                                                        datasetview.AN_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.AN_result.Availability[i]]


    elif (Blood_Group == "OP"):
        for i in range(len(datasetview.OP_result)):
            if (minlatitude <= datasetview.OP_result.Latitude[i] and maxlatitude >= datasetview.OP_result.Latitude[i]) and (
                    minlongitude <= datasetview.OP_result.Longitude[i] and maxlongitude >= datasetview.OP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.OP_result.Serial_No[i]] + [datasetview.OP_result.Latitude[i]] + [
                    datasetview.OP_result.Longitude[i]] + [datasetview.OP_result.Contact_No[i]] + [datasetview.OP_result.Age[i]] + [
                                                        datasetview.OP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.OP_result.Availability[i]]


    elif (Blood_Group == "ON"):
        for i in range(len(datasetview.ON_result)):
            if (minlatitude <= datasetview.ON_result.Latitude[i] and maxlatitude >= datasetview.ON_result.Latitude[i]) and (
                    minlongitude <= datasetview.ON_result.Longitude[i] and maxlongitude >= datasetview.ON_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.ON_result.Serial_No[i]] + [datasetview.ON_result.Latitude[i]] + [
                    datasetview.ON_result.Longitude[i]] + [datasetview.ON_result.Contact_No[i]] + [datasetview.ON_result.Age[i]] + [
                                                        datasetview.ON_result.Date_of_Next_Blood_Donation[i]] + [
                                                        datasetview.ON_result.Availability[i]]


    elif (Blood_Group == "BN"):
        for i in range(len(datasetview.BN_result)):
            if (minlatitude <= datasetview.BN_result.Latitude[i] and maxlatitude >= datasetview.BN_result.Latitude[i]) and (
                    minlongitude <= datasetview.BN_result.Longitude[i] and maxlongitude >= datasetview.BN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [datasetview.BN_result.Serial_No[i]] + [datasetview.BN_result.Latitude[i]] + [
                    datasetview.BN_result.Longitude[i]] + [datasetview.BN_result.Contact_No[i]] + [datasetview.BN_result.Age[i]] + [
                                                        datasetview.BN_result.Date_of_Next_Blood_Donation[i]] + [datasetviewsetview.BN_result.Availability[i]]

    return DONORRESULT_BloodType



@manager.route('/dashbord/manager/bloodrequest')
def bloodRequest():
        bloodRequests=BloodRequest.query.all()
        return render_template('ManagerArea/bloodRequest/index.html', bloodRequests=bloodRequests)
         
@manager.route('/dashbord/manager/bloodrequest/<id>')
def assignBlood(id):
    bloodRequest = BloodRequest.query.filter_by(id=id).first()
    return render_template('ManagerArea/bloodRequest/requestview.html',bloodRequest=bloodRequest)
 
@manager.route('/dashbord/manager/bloodrequest/update', methods=['POST'])
def blood_request_post():

        idValue = request.form.get('id')
        pk_contract_address = request.form.get('pk_contract_address')
        pk_tx_hash = request.form.get('pk_tx_hash')
        dinNo = request.form.get('dinNo')

        bloodRequest = BloodRequest.query.filter_by(id=idValue).first()


        bloodRequest.pk_contract_address = pk_contract_address
        bloodRequest.pk_tx_hash = pk_tx_hash
        bloodRequest.dinNo =  dinNo
        bloodRequest.status =  'true'

        db.session.commit()

        flash("Blood request updated successfully!", 'success')
        return redirect(url_for('manager.bloodRequest'))

# Role route
@manager.route('/dashbord/manager/donor/best/sms', methods=['post'])
def donorSentSms():

        bloodRequest = BloodDonnerRequestNow.query.order_by(BloodDonnerRequestNow.id.desc()).limit(1).first()
        bloodRequestId = bloodRequest.id
        # BloodReuests = request.form.getlist('BloodReuests[]')
        account_sid = "AC2dc90fb5ff6c09288e3e2a581e39751e"
        # Your Auth Token from twilio.com/console
        auth_token = "b4cb884b82ad6c036a438751ef66d7f7"

        client = Client(account_sid, auth_token)
        url = flask.request.host+url_for('donors.requestView',id=bloodRequestId);
        # message = client.messages.create(  
        #                       messaging_service_sid='MG666907fd71bfffd41f39ac1cccfae97b', 
                           
        # body="There is an immediate situation and blood pints required to the hospital. Let us know your response by filling the form.! "+url,      
        #                       to='+94710113861' 
        #                   ) 
                          


        # BloodReuests = request.form.getlist('BloodReuests[]')
        # account_sid = "AC7f8225c500cb386aae697772363b5001"
        # # Your Auth Token from twilio.com/console
        # auth_token = "59f037661bb18f823810cfac612e3d31"

        # client = Client(account_sid, auth_token)
        # url = flask.request.host+url_for('donors.requestView',id=bloodRequestId);
        # message = client.messages.create(
        # to="+94776372733",
        # from_="+14806855803",
        # body="There is an immediate situation and blood pints required to the hospital. Let us know your response by filling the form.! "+url)

        flash("Blood request sms sent successfully!", 'success')
        return redirect(url_for('manager.bestDonor'))