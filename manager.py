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

manager = Blueprint('manager', __name__)
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

# Role route
@manager.route('/dashbord/manager/donor')
def donor():
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        count=0
        
        with open(ROOT_DIR+'/data/Donors.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                first_line = True
                data_list = []
                for row in data:
                        if not first_line:
                                if (count<500):
                                        data_list.append({
                                        "fullname": row[1],
                                        "id": row[0],
                                        "gender": row[4],
                                        "blood_group": row[15],
                                        })
                                        count=count+1
                                
                        else:
                                first_line = False
                                
        donors=Donor.query.all()
        return render_template('ManagerArea/Donor/index.html',donors=donors)

@manager.route('/dashbord/manager/donor/add')
def donorAdd():
        return render_template('ManagerArea/Donor/add.html')

@manager.route('/dashbord/manager/donor/add', methods=['POST'])
def donor_post():

        email = request.form.get('email')
        NIC_no = request.form.get('NIC_no')
        fullname = request.form.get('fullname')
        name =  request.form.get('name')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        weight =  request.form.get('weight')
        height = request.form.get('height')
        blood_group = request.form.get('blood_group')
        contact_no =  request.form.get('contact_no')
        address =  request.form.get('address')

        
        user = User.query.filter_by(email=email).first() 

        if user: 
                flash("Email address already exists!", 'warning')
                return redirect(url_for('manager.donorAdd'))

        user = User.query.filter_by(NIC_no=NIC_no).first() 
        
        if user: 
                flash("NIC no already exists!", 'warning')
                return redirect(url_for('manager.donorAdd'))

        donor = Donor.query.filter_by(NIC_no=NIC_no).first() 
        
        if donor: 
                flash("NIC no already exists!", 'warning')
                return redirect(url_for('manager.donorAdd'))
        birthday = datetime.strptime(birthday, '%Y-%m-%d')

        password = NIC_no
        
        new_user = User(email=email, name=fullname, password=generate_password_hash(password, method='sha256'))
        role1 =Role.query.filter_by(name='donor').first()
        
        new_user.roles.append(role1)
        
        db.session.add(new_user)
        db.session.commit()


        geocoder = GoogleGeocoder("AIzaSyCpF7lrlIVgAczW0DLYpfs2VNalLvFJ_LU")
        search = geocoder.get(address)


        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_donor = Donor(
                email=email, 
                NIC_no=NIC_no,
                fullname=fullname, 
                name=fullname,
                birthday=birthday, 
                gender=gender,
                weight=weight, 
                height=height,
                blood_group=blood_group, 
                contact_no=contact_no,
                address=address,
                longitude=search[0].geometry.location.lng,
                latitude=search[0].geometry.location.lat,
                )
        db.session.add(new_donor)
        db.session.commit()

        flash("Donor details added successfully!", 'success')
        return redirect(url_for('manager.donor'))

# Role route
@manager.route('/dashbord/manager/donor/<int:user_id>/view', methods=['GET'])
def donorview(user_id):
        donor = Donor.query.filter_by(id=user_id).first()
        birthday = datetime.date(donor.birthday)
        birthday = birthday.strftime('%Y-%m-%d')
        donor.birthday=birthday
        return render_template('ManagerArea/Donor/view.html',donor=donor)

# Role route
@manager.route('/dashbord/manager/donor/<int:user_id>/edit', methods=['GET'])
def donoredit(user_id):
        donor = Donor.query.filter_by(id=user_id).first()
        birthday = datetime.date(donor.birthday)
        birthday = birthday.strftime('%Y-%m-%d')
        donor.birthday=birthday
        return render_template('ManagerArea/Donor/edit.html',donor=donor)

@manager.route('/dashbord/manager/donor/update', methods=['POST'])
def donor_update_post():

        user_id = request.form.get('id')

        donor = Donor.query.filter_by(id=user_id).first()
        email = request.form.get('email')
        NIC_no = request.form.get('NIC_no')
        fullname = request.form.get('fullname')
        name =  request.form.get('name')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        weight =  request.form.get('weight')
        height = request.form.get('height')
        blood_group = request.form.get('blood_group')
        contact_no =  request.form.get('contact_no')
        address =  request.form.get('address')

        
        user = User.query.filter_by(email=email).first() 

        if (donor.email!=email):
                if user: 
                        flash("Email address already exists!", 'warning')
                        return redirect(url_for('manager.donoredit'))

                user = User.query.filter_by(NIC_no=NIC_no).first() 
                
                if user: 
                        flash("NIC no already exists!", 'warning')
                        return redirect(url_for('manager.donoredit'))

        donor = Donor.query.filter_by(NIC_no=NIC_no).first() 
        
        birthday = datetime.strptime(birthday, '%Y-%m-%d')

        password = NIC_no
        
        user.email=email
        user.name=fullname
        user.password=generate_password_hash(password, method='sha256')
        db.session.commit()

        geocoder = GoogleGeocoder("AIzaSyCpF7lrlIVgAczW0DLYpfs2VNalLvFJ_LU")
        search = geocoder.get(address)


        donor.email = email
        donor.NIC_no = NIC_no
        donor.fullname = fullname
        donor.name =  name
        donor.birthday = birthday
        donor.gender = gender
        donor.weight =  weight
        donor.height = height
        donor.blood_group = blood_group
        donor.contact_no =  contact_no
        donor.address =  address
        donor.longitude=search[0].geometry.location.lng
        donor.latitude=search[0].geometry.location.lat

        db.session.commit()

        flash("Donor details updated successfully!", 'success')
        return redirect(url_for('manager.donor'))

@manager.route('/dashbord/manager')
def dashbord():
        return render_template('ManagerArea/index.html')

# Role route
@manager.route('/dashbord/manager/donor/<int:user_id>/delete', methods=['GET'])
def donordelete(user_id):
        donor = Donor.query.filter_by(id=user_id).first()
        db.session.delete(donor)
        db.session.commit()
        flash("Donor details deleted successfully!", 'success')
        return redirect(url_for('manager.donor'))

@manager.route('/dashbord/manager/bloodstore')
def bloodstore():
        packets=BloodPacket.query.all()
        return render_template('ManagerArea/BloodStore/index.html',packets=packets)
        

@manager.route('/dashbord/manager/bloodstore/add')
def bloodstoreAdd():
        donors=Donor.query.all()
        return render_template('ManagerArea/BloodStore/add.html',donors=donors)

@manager.route('/dashbord/manager/blooddemand')
def blooddemand():

        first_line = True
        data_list = []
        count_list = []
        iddata=0
        AllCount=[]
        ACount=[]
        BCount=[]
        OCount=[]
        ABCount=[]
        NCount=[]
        with open(ROOT_DIR+'/datamodel/all.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                for row in data:
                        if not first_line:
                                AllCount.append(int(row[1]))
                                ACount.append(int(row[6]))
                                BCount.append(int(row[4]))
                                OCount.append(int(row[2]))
                                ABCount.append(int(row[8]))
                                NCount.append(int(row[3])+int(row[5])+int(row[7])+int(row[9]))
                                iddata=iddata+1
                                data_list.append({
                                "id": (iddata),
                                "Date": row[0],
                                "All": row[1],
                                "OP": row[2],
                                "ON": row[3],
                                "BP": row[4],
                                "BN": row[5],
                                "AP": row[6],
                                "AN": row[7],
                                "ABP": row[8],
                                "ABN": row[9]
                                })
                                
                        else:
                                first_line = False
        count_list = [sum(AllCount),sum(ACount),sum(BCount),sum(OCount),sum(ABCount),sum(NCount)]     
        return render_template('ManagerArea/Blooddemand/index.html',data_list=data_list,count_list=count_list)

@manager.route('/dashbord/manager/blooddemand/get', methods=['POST'])
def blooddemand_post():
        
        bloodgrop = request.form.get('bloodgrop')
        model = keras.models.load_model(ROOT_DIR+"/datamodel/"+bloodgrop+"model.h5")
        transformer = joblib.load(ROOT_DIR+"/datamodel/"+bloodgrop+"data_transformer.joblib")
        
        df= LoadPastDataset(bloodgrop)
        dft= transformer.transform(df)
        batch = dft[-4:].reshape((1,4,1))
        pred_list = []
        for i in range(4):  
                pred_list.append(model.predict(batch)[0])
                batch = np.append(batch[:,1:,:],[[pred_list[i]]],axis=1)
        add_dates = [df.index[-1] + DateOffset(weeks=x) for x in range(0,5) ]
        future_dates = pd.DataFrame(index=add_dates[1:],columns=df.columns)
        df_predict = pd.DataFrame(transformer.inverse_transform(pred_list),
                                index=future_dates[-4:].index, columns=['Prediction'])
        df_proj = pd.concat([df,df_predict], axis=1)
        df_proj.index.name ='Date'
        df_proj.reset_index(inplace=True)
        df_proj['Date'].to_list()
        df_proj['Date']=df_proj['Date'].astype(str)
        dateList = df_proj['Date'].to_list()
        Prediction = df_predict["Prediction"].tolist()
        Data = df[bloodgrop].tolist()
        P1 = Prediction[0]
        P2 = Prediction[1]
        P3 = Prediction[2]
        P4 = Prediction[3]
        
        return render_template('ManagerArea/Blooddemand/view.html',dateList=dateList,Data=Data,P4=P4,P3=P3,P2=P2,P1=P1,Prediction=Prediction)

@manager.route('/dashbord/manager/bloodcamp')
def bloodcamp():
        
        with open(ROOT_DIR+'/data/clustered_data.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                first_line = True
                data_list = []
                CampClusterData = []
                Campdata = []
                for row in data:
                        if not first_line:
                                data_list.append({
                                "SerialNo": row[0],
                                "FullName": row[1],
                                "DateofBirth": row[2],
                                "Age": row[3],
                                "Gender": row[4],
                                "Weight": row[5],
                                "Height": row[6],
                                "ContactNo": row[7],
                                "PreDonation": row[8],
                                "NextDonation": row[9],
                                "Availability": row[10],
                                "Longitude_x": row[11],
                                "Latitude_x": row[12],
                                "Address": row[13],
                                "NICNo": row[14],
                                "BloodGroup": row[15],
                                "DonatedCampaign": row[16],
                                "CampClusterLabel": row[17],
                                "CampLatitude": row[18],
                                "CampLongitude": row[19],
                                "CampAddress": row[20]
                                })
                                CampClusterLabel=row[17]
                                if CampClusterLabel not in CampClusterData:
                                        CampClusterData.append(row[17])
                                        Campdata.append({"CampClusterLabel": row[17],"CampAddress": row[20],"CampLatitude": row[18],"CampLongitude": row[19]})
                        else:
                                first_line = False
                                
        return render_template("ManagerArea/BloodCamp/index.html",CampAddress=Campdata,data_list=data_list)

@manager.route('/dashbord/manager/bloodcamp/get', methods=['POST'])
def bloodcamp_post():
        CampCluster = request.form.get('CampCluster')
        
        ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
        
        with open(ROOT_DIR+'/data/clustered_data.csv') as csv_file:
                data = csv.reader(csv_file, delimiter=',')
                first_line = True
                data_list = []
                CampClusterData = []
                Campdata = []
                CampFind = []
                CampAll = []
                CountOfDonor=0
                CountOfUniqDonor=0
                for row in data:
                        if not first_line:
                                if  (row[17]==CampCluster):
                                        itemData = {'position': 'new google.maps.LatLng('+row[11]+','+row[12]+')',
				                'type': 'donor'}
                                        CampFind.append(itemData)
                                        data_list.append({
                                        "SerialNo": row[0],
                                        "FullName": row[1],
                                        "DateofBirth": row[2],
                                        "Age": row[3],
                                        "Gender": row[4],
                                        "Weight": row[5],
                                        "Height": row[6],
                                        "ContactNo": row[7],
                                        "PreDonation": row[8],
                                        "NextDonation": row[9],
                                        "Availability": row[10],
                                        "Longitude_x": row[11],
                                        "Latitude_x": row[12],
                                        "Address": row[13],
                                        "NICNo": row[14],
                                        "BloodGroup": row[15],
                                        "DonatedCampaign": row[16],
                                        "CampClusterLabel": row[17],
                                        "CampLatitude": row[18],
                                        "CampLongitude": row[19],
                                        "CampAddress": row[20]
                                        })
                                        CampLongitude=row[19]
                                        CampLatitude=row[18]
                                        CountOfUniqDonor = CountOfUniqDonor + 1
                                CampClusterLabel=row[17]
                                CampAll.append(row[17])
                                if CampClusterLabel not in CampClusterData:
                                        CampClusterData.append(row[17])
                                        Campdata.append({"CampClusterLabel": row[17],"CampAddress": row[20]})
                        else:
                                first_line = False
                        
        for uniqcamp in CampAll:
                if  (uniqcamp==CampCluster):
                        CountOfDonor = CountOfDonor + 1
                        
        jsonData=json.dumps(CampFind)


        return render_template("ManagerArea/BloodCamp/view.html",CampLongitude=CampLongitude,CampLatitude=CampLatitude,data_list=data_list,CampAddress=Campdata,CampCluster=CampCluster,CountOfDonor=CountOfDonor,jsonData=jsonData)


@manager.route('/dashbord/manager/donor/best')
def bestDonor():
        BloodReuests=BloodDonnerRequestNow.query.all()
        return render_template('ManagerArea/Donor/bestIndex.html',BloodReuests=BloodReuests)

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
                          

        print("##############")
        print("request URL")
        print(url)
        print("##############")

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