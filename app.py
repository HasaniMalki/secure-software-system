import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import data

from flask import Flask
from flask import request
from datetime import date

app = Flask(__name__)


@app.route('/aaa')
def hello_world():
    today = date.today()

    df = pd.DataFrame({'DOB': {0: '1/26/2016', 1: '26/1/2016'}})
    print(df)
    df['DOB'] = pd.to_datetime(df.DOB)
    print(df)
    print("Today's date:", today)
    return "abc"


@app.route('/bestDonor')
def findBestDonor():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    stage = int(request.args.get('stage'))
    Blood_Group = str(request.args.get('Blood_Group'))
    count = int(request.args.get('Count'))

    #  print(Blood_Group)

    maxlatitude = maxlat(latitude, stage)
    minlatitude = minlat(latitude, stage)
    maxlongitude = maxlon(longitude, stage)
    minlongitude = minlon(longitude, stage)


    # ////////////////////////////////////////////////////////////// Selecting suitable donors according to the stages

    DONORRESULT_BloodType = bestDonor(Blood_Group,minlatitude,maxlatitude,minlongitude,maxlongitude)
    print(Blood_Group)

    DONORRESULT_BloodType = DONORRESULT_BloodType.reset_index()
    # print(DONORRESULT_BloodType)


    # ////////////////////////////////////////////////////////////////////////// Check availability, age and next blood donation date
    Available_DONORRESULT_BloodType = data.Available_DONORRESULT_BloodType
    Available_DONORRESULT_BloodType = Available_DONORRESULT_BloodType.iloc[0:0]


    for i in range(len(DONORRESULT_BloodType)):
        today = date.today()
        nextbloodDOnationDate = pd.to_datetime(DONORRESULT_BloodType.Date_of_Next_Blood_Donation[i])
        if (DONORRESULT_BloodType.Age[i] <= 60 and DONORRESULT_BloodType.Availability[i] == 'Available' and nextbloodDOnationDate < today):
                Available_DONORRESULT_BloodType.loc[i] = [DONORRESULT_BloodType.Serial_No[i]] + [
                DONORRESULT_BloodType.Latitude[i]] + [DONORRESULT_BloodType.Longitude[i]] + [DONORRESULT_BloodType.Contact_No[i]]


   # Available_DONORRESULT_BloodType = data.Available_DONORRESULT_BloodType.reset_index()
    Available_DONORRESULT_BloodType = Available_DONORRESULT_BloodType.reset_index()

    # /////////////////////////////////////////////////////////////////// Mathematical process

    Distance_KM = data.Distance_KM
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



 #   print(Distance_KM)
    Final_list = Distance_KM.sort_values(by=['Distance']).reset_index().head(count)
    Final = Final_list.reset_index().values.tolist()
    for Finals in Final:
        print(Finals[2])
  #  Final_list = Final_list.iloc[0:0]
    return "Final li"




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
    # /////////////////////////////////////////////////////////////// Create function for compare locations between donors and the hospital
    DONORRESULT_BloodType = data.DONORRESULT_BloodType
    DONORRESULT_BloodType = DONORRESULT_BloodType.iloc[0:0]

    if (Blood_Group == "ABN"):
        for i in range(len(data.ABN_result)):
            if (minlatitude <= data.ABN_result.Latitude[i] and maxlatitude >= data.ABN_result.Latitude[i]) and (
                    minlongitude <= data.ABN_result.Longitude[i] and maxlongitude >= data.ABN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.ABN_result.Serial_No[i]] + [data.ABN_result.Latitude[i]] + [
                    data.ABN_result.Longitude[i]] + [data.ABN_result.Contact_No[i]] + [data.ABN_result.Age[i]] + [
                                                        data.ABN_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.ABN_result.Availability[i]]

    elif (Blood_Group == "AP"):
        for i in range(len(data.AP_result)):
            if (minlatitude <= data.AP_result.Latitude[i] and maxlatitude >= data.AP_result.Latitude[i]) and (
                    minlongitude <= data.AP_result.Longitude[i] and maxlongitude >= data.AP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.AP_result.Serial_No[i]] + [data.AP_result.Latitude[i]] + [
                    data.AP_result.Longitude[i]] + [data.AP_result.Contact_No[i]] + [data.AP_result.Age[i]] + [
                                                        data.AP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.AP_result.Availability[i]]

    elif (Blood_Group == "BP"):
        for i in range(len(data.BP_result)):
            if (minlatitude <= data.BP_result.Latitude[i] and maxlatitude >= data.BP_result.Latitude[i]) and (
                    minlongitude <= data.BP_result.Longitude[i] and maxlongitude >= data.BP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.BP_result.Serial_No[i]] + [data.BP_result.Latitude[i]] + [
                    data.BP_result.Longitude[i]] + [data.BP_result.Contact_No[i]] + [data.BP_result.Age[i]] + [
                                                        data.BP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.BP_result.Availability[i]]

    elif (Blood_Group == "ABP"):
        for i in range(len(data.ABP_result)):
            if (minlatitude <= data.ABP_result.Latitude[i] and maxlatitude >= data.ABP_result.Latitude[i]) and (
                    minlongitude <= data.ABP_result.Longitude[i] and maxlongitude >= data.ABP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.ABP_result.Serial_No[i]] + [data.ABP_result.Latitude[i]] + [
                    data.ABP_result.Longitude[i]] + [data.ABP_result.Contact_No[i]] + [data.ABP_result.Age[i]] + [
                                                        data.ABP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.ABP_result.Availability[i]]


    elif (Blood_Group == "AN"):
        for i in range(len(data.AN_result)):
            if (minlatitude <= data.AN_result.Latitude[i] and maxlatitude >= data.AN_result.Latitude[i]) and (
                    minlongitude <= data.AN_result.Longitude[i] and maxlongitude >= data.AN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.AN_result.Serial_No[i]] + [data.AN_result.Latitude[i]] + [
                    data.AN_result.Longitude[i]] + [data.AN_result.Contact_No[i]] + [data.AN_result.Age[i]] + [
                                                        data.AN_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.AN_result.Availability[i]]


    elif (Blood_Group == "OP"):
        for i in range(len(data.OP_result)):
            if (minlatitude <= data.OP_result.Latitude[i] and maxlatitude >= data.OP_result.Latitude[i]) and (
                    minlongitude <= data.OP_result.Longitude[i] and maxlongitude >= data.OP_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.OP_result.Serial_No[i]] + [data.OP_result.Latitude[i]] + [
                    data.OP_result.Longitude[i]] + [data.OP_result.Contact_No[i]] + [data.OP_result.Age[i]] + [
                                                        data.OP_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.OP_result.Availability[i]]


    elif (Blood_Group == "ON"):
        for i in range(len(data.ON_result)):
            if (minlatitude <= data.ON_result.Latitude[i] and maxlatitude >= data.ON_result.Latitude[i]) and (
                    minlongitude <= data.ON_result.Longitude[i] and maxlongitude >= data.ON_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.ON_result.Serial_No[i]] + [data.ON_result.Latitude[i]] + [
                    data.ON_result.Longitude[i]] + [data.ON_result.Contact_No[i]] + [data.ON_result.Age[i]] + [
                                                        data.ON_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.ON_result.Availability[i]]


    elif (Blood_Group == "BN"):
        for i in range(len(data.BN_result)):
            if (minlatitude <= data.BN_result.Latitude[i] and maxlatitude >= data.BN_result.Latitude[i]) and (
                    minlongitude <= data.BN_result.Longitude[i] and maxlongitude >= data.BN_result.Longitude[i]):
                DONORRESULT_BloodType.loc[i] = [data.BN_result.Serial_No[i]] + [data.BN_result.Latitude[i]] + [
                    data.BN_result.Longitude[i]] + [data.BN_result.Contact_No[i]] + [data.BN_result.Age[i]] + [
                                                        data.BN_result.Date_of_Next_Blood_Donation[i]] + [
                                                        data.BN_result.Availability[i]]

    return DONORRESULT_BloodType

    # print(len(DONORRESULT_BloodType))


if __name__ == '__main__':
    app.run(debug=True)
