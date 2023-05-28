from flask_login import UserMixin
from . import db
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    NIC_no = db.Column(db.String(1000), unique=True)
    roles = db.relationship('Role', secondary='user_roles',
            backref=db.backref('users', lazy='dynamic'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define Role model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define UserRoles model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define Donor model
class Donor( db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    NIC_no = db.Column(db.String(1000), unique=True)
    fullname = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    birthday = db.Column(db.DateTime())
    gender = db.Column(db.String(100))
    weight = db.Column(db.Integer())
    height = db.Column(db.Integer())
    blood_group = db.Column(db.String(100))
    contact_no = db.Column(db.String(100))
    pre_donation = db.Column(db.DateTime(), nullable=True)
    Next_donation = db.Column(db.DateTime(), nullable=True)
    blood_campaign = db.Column(db.String(200), nullable=True)
    address = db.Column(db.Text())
    longitude = db.Column(db.String(1000))
    latitude = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
# Define BloodCampaign model
class BloodCampaign( db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(1000))
    OrganizedDate = db.Column(db.DateTime())
    address = db.Column(db.Text())
    longitude = db.Column(db.String(1000))
    latitude = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define Donor model
class Hospital( db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    name = db.Column(db.String(1000))
    address = db.Column(db.Text())
    contact_no = db.Column(db.String(100))
    longitude = db.Column(db.String(1000))
    latitude = db.Column(db.String(1000))
    contract_address= db.Column(db.String(1000))
    tx_hash= db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
# Define Patient model
class Patient( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    NIC_no = db.Column(db.String(1000), unique=True)
    name = db.Column(db.String(1000))
    birthday = db.Column(db.DateTime())
    gender = db.Column(db.String(100))
    weight = db.Column(db.Integer())
    height = db.Column(db.Integer())
    blood_group = db.Column(db.String(100))
    contact_no = db.Column(db.String(100))
    Availability=db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BloodPacket model
class BloodPacket( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(100))
    test = db.Column(db.String(100))
    donnor_id = db.Column(db.String(100))
    test_id = db.Column(db.String(100))
    expire_date = db.Column(db.DateTime())
    issued_date= db.Column(db.DateTime())
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BloodTest model
class BloodTest( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    haemoglobin = db.Column(db.String(100))
    WBC_count = db.Column(db.String(100))
    haematocrit = db.Column(db.String(100))
    platelet_count = db.Column(db.String(100))
    MPV= db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BloodIssued model
class BloodIssued( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    donnor_id = db.Column(db.String(100))
    patinet_id = db.Column(db.String(100))
    doctor_id = db.Column(db.String(100))
    blood_pk_id = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BloodReuestDoctor model
class BloodReuestDoctor( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(100))
    reason = db.Column(db.String(100))
    patinet_id = db.Column(db.String(100))
    doctor_id = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BloodReuestDonnor model
class BloodReuestDonnor( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status_join= db.Column(db.String(100), nullable=True)
    status_disease= db.Column(db.String(100), nullable=True)
    weight = db.Column(db.String(100), nullable=True)
    donnor_id = db.Column(db.String(100))
    request_id = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BestDonnor model
class BestDonnor( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    blood_group = db.Column(db.String(100))
    reason = db.Column(db.String(100))
    number_of_donnors = db.Column(db.String(100))
    hospital_id = db.Column(db.String(100))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define Doctor model
class Doctor( db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100))
    NIC_no = db.Column(db.String(1000), unique=True)
    fullname = db.Column(db.String(1000))
    name = db.Column(db.String(1000))
    hospital_id = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)

# Define BestDonnor model
class BloodRequest( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hospital_id = db.Column(db.String(100))
    pnic = db.Column(db.String(1000))
    pname = db.Column(db.String(1000))
    pphone = db.Column(db.String(1000))
    reason = db.Column(db.String(1000))
    age = db.Column(db.String(1000))
    bloodtype = db.Column(db.String(1000))
    dID = db.Column(db.String(1000))
    dname = db.Column(db.String(1000))
    dinNo = db.Column(db.String(1000))
    status = db.Column(db.String(1000))
    contract_address= db.Column(db.String(1000))
    tx_hash= db.Column(db.String(1000))
    pk_contract_address= db.Column(db.String(1000))
    pk_tx_hash= db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)

class BloodDonnerRequestNow( db.Model):
    id = db.Column(db.Integer, primary_key=True)
    s_number = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    distance = db.Column(db.String(100))
    status = db.Column(db.String(100))
    contact = db.Column(db.String(100))
    disease = db.Column(db.String(1000))
    weight = db.Column(db.String(1000))
    time = db.Column(db.String(1000))
    created = db.Column(db.DateTime, default=datetime.utcnow)
    