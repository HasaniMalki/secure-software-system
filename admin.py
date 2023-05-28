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
from .models import User,Role,UserRoles,Donor,Hospital,BloodCampaign,Doctor
from geopy.geocoders import Nominatim
from datetime import datetime
from googlegeocoder import GoogleGeocoder
import csv
import json
from twilio.rest import Client
admin = Blueprint('admin', __name__)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


@admin.before_request
def before_request():
    if not current_user.is_authenticated :
        flash('Please login first.')
        return redirect(url_for('auth.login'))
    userroles=UserRoles.query.filter_by(user_id=current_user.id).first()
    userrole=Role.query.filter_by(id=userroles.role_id).first()
    if (userrole.name!="admin"):
        return redirect(url_for('auth.permission'))

# # #  Route for admin # # # 
@admin.route('/dashbord/admin')
def dashbord():
        return render_template('AdminArea/index.html')

# # #  Route for user # # # 
@admin.route('/dashbord/admin/user')
def user():
        users=User.query.all()
        return render_template('AdminArea/User/index.html',users=users)
        
@admin.route('/dashbord/admin/user/<id>')
def userView(id):
  return "The product is " + str(id)

@admin.route('/dashbord/admin/user/add')
def userAdd():
        roles=Role.query.all()
        return render_template('AdminArea/User/add.html',roles=roles)

@admin.route('/dashbord/admin/user/add', methods=['POST'])
def user_post():
    email = request.form.get('useremail')
    name = request.form.get('username')
    role = request.form.get('role')
    NIC_no = request.form.get('NIC_no')
    password = NIC_no

    user = User.query.filter_by(email=email).first() 
    
    if user: 
        flash("Email address already exists!", 'warning')
        return redirect(url_for('admin.userAdd'))

    user = User.query.filter_by(NIC_no=NIC_no).first() 
    
    if user: 
        flash("NIC no already exists!", 'warning')
        return redirect(url_for('admin.userAdd'))


    new_user = User(email=email, name=name, NIC_no=NIC_no, password=generate_password_hash(password, method='sha256'))
    role1 =Role.query.filter_by(name=role).first()
    new_user.roles.append(role1)
    db.session.add(new_user)
    print('dataset.id')
    db.session.commit()

    flash("User added successfully!", 'success')
    return redirect(url_for('admin.user'))


# # #  Route for donor # # # 
@admin.route('/dashbord/admin/donor')
def donor():
        donors=Donor.query.all()
        return render_template('AdminArea/Donor/index.html',donors=donors)

@admin.route('/dashbord/admin/donor/add')
def donorAdd():
        return render_template('AdminArea/Donor/add.html')

@admin.route('/dashbord/admin/donor/add', methods=['POST'])
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
        return redirect(url_for('admin.donorAdd'))

    user = User.query.filter_by(NIC_no=NIC_no).first() 
    
    if user: 
        flash("NIC no already exists!", 'warning')
        return redirect(url_for('admin.donorAdd'))

    donor = Donor.query.filter_by(NIC_no=NIC_no).first() 
    
    birthday = datetime.strptime(birthday, '%Y-%m-%d')

    password = NIC_no
    
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
    role1 =Role.query.filter_by(name='donor').first()
    
    new_user.roles.append(role1)
    
    db.session.add(new_user)
    db.session.commit()

    if donor: 
        flash("NIC no already exists!", 'warning')
        return redirect(url_for('admin.donorAdd'))

    geolocator = Nominatim(user_agent="AIMA")
    location = geolocator.geocode("175 5th Avenue NYC")

    geocoder = GoogleGeocoder("AIzaSyCpF7lrlIVgAczW0DLYpfs2VNalLvFJ_LU")
    search = geocoder.get(address)


    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_donor = Donor(
        email=email, 
        NIC_no=NIC_no,
        fullname=fullname, 
        name=name,
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

    flash("Donoer added successfully!", 'success')
    return redirect(url_for('admin.donor'))
        
# # #  Route for hospital # # # 
@admin.route('/dashbord/hospital')
def hospital():
        hospitals=Hospital.query.all()
        return render_template('AdminArea/Hospital/index.html',hospitals=hospitals)

@admin.route('/dashbord/admin/hospital/add')
def hospitalAdd():
        hospital = Hospital.query.order_by(Hospital.id.desc()).first();
        return render_template('AdminArea/Hospital/add.html',hospital=hospital)

@admin.route('/dashbord/admin/hospital/add', methods=['POST'])
def hospital_post():

    idVal = request.form.get('idVal')
    name = request.form.get('name')
    address = request.form.get('address')
    contact_no =  request.form.get('contact_no')
    contract_address =  request.form.get('contract_address')
    tx_hash =  request.form.get('tx_hash')

    geocoder = GoogleGeocoder("AIzaSyCpF7lrlIVgAczW0DLYpfs2VNalLvFJ_LU")
    search = geocoder.get(address)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_hospital= Hospital(
        id=idVal, 
        name=name, 
        address=address,
        contact_no=contact_no, 
        longitude=search[0].geometry.location.lng,
        latitude=search[0].geometry.location.lat,
        contract_address=contract_address,
        tx_hash=tx_hash,
        )
    db.session.add(new_hospital)
    db.session.commit()

    flash("Hospital added successfully!", 'success')
    return redirect(url_for('admin.hospital'))
        
# # #  Route for bloodcampaign # # #
@admin.route('/dashbord/bloodcampaign')
def bloodcampaign():
        bloodcampaigns=BloodCampaign.query.all()
        return render_template('AdminArea/Bloodchamp/index.html', bloodcampaigns=bloodcampaigns)

@admin.route('/dashbord/admin/bloodcampaign/add')
def bloodcampaignFirstAdd():
        return render_template('AdminArea/Bloodchamp/addindex.html')

@admin.route('/dashbord/admin/bloodcampaign/add/new')
def bloodcampaignAdd():
        return render_template('AdminArea/Bloodchamp/add.html')

@admin.route('/dashbord/admin/bloodcampaign/add', methods=['POST'])
def bloodcampaign_post():

    name = request.form.get('name')
    address = request.form.get('address')
    contact_no =  request.form.get('contact_no')
    OrganizedDate = request.form.get('OrganizedDate')

    OrganizedDate = datetime.strptime(OrganizedDate, '%Y-%m-%d')
    geocoder = GoogleGeocoder("AIzaSyCpF7lrlIVgAczW0DLYpfs2VNalLvFJ_LU")
    search = geocoder.get(address)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_bloodcampaign= BloodCampaign(
        name=name, 
        address=address,
        OrganizedDate=OrganizedDate, 
        longitude=search[0].geometry.location.lng,
        latitude=search[0].geometry.location.lat,
        )
    db.session.add(new_bloodcampaign)
    db.session.commit()

    flash("Blood bank added successfully!", 'success')
    return redirect(url_for('admin.bloodcampaign'))


@admin.route('/dashbord/admin/bloodcamp/index')
def BestCampaign():
        
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

                                
        return render_template("AdminArea/Bloodchamp/campindex.html",CampAddress=Campdata,data_list=data_list)

@admin.route('/dashbord/admin/bloodcamp/get', methods=['POST'])
def bloodcamp_view():
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


        return render_template("AdminArea/Bloodchamp/campview.html",CampLongitude=CampLongitude,CampLatitude=CampLatitude,data_list=data_list,CampAddress=Campdata,CampCluster=CampCluster,CountOfDonor=CountOfDonor,jsonData=jsonData)


# # #  Route for doctor # # # 
@admin.route('/dashbord/admin/doctor')
def doctor():
        doctors=Doctor.query.all()
        hospitals=Hospital.query.all()
        return render_template('AdminArea/Doctor/index.html',doctors=doctors,hospitals=hospitals)
        
@admin.route('/dashbord/admin/doctor/<id>')
def doctorView(id):
  return "The product is " + str(id)

@admin.route('/dashbord/admin/doctor/add')
def doctorAdd():
        hospitals=Hospital.query.all()
        return render_template('AdminArea/Doctor/add.html',hospitals=hospitals)

@admin.route('/dashbord/admin/doctor/add', methods=['POST'])
def doctor_post():

        email = request.form.get('email')
        NIC_no = request.form.get('NIC_no')
        fullname = request.form.get('fullname')
        name =  request.form.get('name')
        hospital_id = request.form.get('hospital_id')
        
        user = User.query.filter_by(email=email).first() 

        if user: 
                flash("Email address already exists!", 'warning')
                return redirect(url_for('admin.doctorAdd'))

        user = User.query.filter_by(NIC_no=NIC_no).first() 
        
        if user: 
                flash("NIC no already exists!", 'warning')
                return redirect(url_for('admin.doctorAdd'))

        password = NIC_no
        
        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        role1 =Role.query.filter_by(name='doctor').first()
        
        new_user.roles.append(role1)
        
        db.session.add(new_user)
        db.session.commit()

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_doctor = Doctor(
                email=email, 
                NIC_no=NIC_no,
                fullname=fullname, 
                name=name,
                hospital_id=hospital_id
                );
        db.session.add(new_doctor)
        db.session.commit()

        flash("Doctor added successfully!", 'success')
        return redirect(url_for('admin.doctor'))