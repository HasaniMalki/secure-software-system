import pandas as pd
import math

import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# //////////////////////////////////////////////////////////////////////////////// Read Data

donor = pd.read_csv(ROOT_DIR+"/data/Donors.csv")
# print(donor)
hospital = pd.read_csv(ROOT_DIR+"/data/Hospitals.csv")
# print(hospital)


# /////////////////////////////////////////////////////////////////////////////// Divide data set for blood group

sp = donor['Blood Group'].unique()
# print(sp)
for value in sp:
    OP = donor[donor['Blood Group'] == "O+"]
# print(OP)

for value in sp:
    AP = donor[donor['Blood Group'] == "A+"]
# print(len(AP))

for value in sp:
    BP = donor[donor['Blood Group'] == "B+"]
# print(len(BP))

for value in sp:
    ABP = donor[donor['Blood Group'] == "AB+"]
# print(len(ABP))

for value in sp:
    AN = donor[donor['Blood Group'] == "A-"]
# print(len(AN))

for value in sp:
    ABN = donor[donor['Blood Group'] == "AB-"]
# print(len(ABN))

for value in sp:
    ON = donor[donor['Blood Group'] == "O-"]
# print(len(ON))

for value in sp:
    BN = donor[donor['Blood Group'] == "B-"]
# print(len(BN))

 # ////////////////////////////////////////////////////////////////// Separate useful data(Donor) using dataframes

    d_AP_lat = AP['Latitude']
    d_AP_lon = AP['Longitude']
    d_AP_sNO = AP['Serial_No']
    d_AP_contactNo = AP['Contact_No']
    d_AP_DOB = AP['Date_of_Birth']
    d_AP_age = AP['Age']
    d_AP_DOfPreviousBD = AP['Date_of_Previous_Blood_Donation']
    d_AP_DOfNextBD = AP['Date_of_Next_Blood_Donation']
    d_AP_availability = AP['Availability']
    d_AP_Name = AP['Full_Name']
    dAP_lat_df1 = pd.DataFrame(d_AP_lat)
    dAP_lon_df2 = pd.DataFrame(d_AP_lon)
    dAP_sNO_df3 = pd.DataFrame(d_AP_sNO)
    dAP_cNO_df4 = pd.DataFrame(d_AP_contactNo)
    dAP_dofb_df5 = pd.DataFrame(d_AP_DOB)
    dAP_age_df6 = pd.DataFrame(d_AP_age)
    dAP_dOfpbd_df7 = pd.DataFrame(d_AP_DOfPreviousBD)
    dAP_dOfnbd_df8 = pd.DataFrame(d_AP_DOfNextBD)
    dAP_available_df9 = pd.DataFrame(d_AP_availability)
    dAP_name_df10 = pd.DataFrame(d_AP_Name)
    AP_result = pd.concat(
        [dAP_sNO_df3, dAP_lat_df1, dAP_lon_df2, dAP_cNO_df4, dAP_dofb_df5, dAP_age_df6, dAP_dOfpbd_df7, dAP_dOfnbd_df8,
         dAP_available_df9, dAP_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_BP_lat = BP['Latitude']
    d_BP_lon = BP['Longitude']
    d_BP_sNO = BP['Serial_No']
    d_BP_contactNo = BP['Contact_No']
    d_BP_DOB = BP['Date_of_Birth']
    d_BP_age = BP['Age']
    d_BP_DOfPreviousBD = BP['Date_of_Previous_Blood_Donation']
    d_BP_DOfNextBD = BP['Date_of_Next_Blood_Donation']
    d_BP_availability = BP['Availability']
    d_BP_Name = BP['Full_Name']
    dBP_lat_df1 = pd.DataFrame(d_BP_lat)
    dBP_lon_df2 = pd.DataFrame(d_BP_lon)
    dBP_sNO_df3 = pd.DataFrame(d_BP_sNO)
    dBP_cNO_df4 = pd.DataFrame(d_BP_contactNo)
    dBP_dofb_df5 = pd.DataFrame(d_BP_DOB)
    dBP_age_df6 = pd.DataFrame(d_BP_age)
    dBP_dOfpbd_df7 = pd.DataFrame(d_BP_DOfPreviousBD)
    dBP_dOfnbd_df8 = pd.DataFrame(d_BP_DOfNextBD)
    dBP_available_df9 = pd.DataFrame(d_BP_availability)
    dBP_name_df10 = pd.DataFrame(d_BP_Name)
    BP_result = pd.concat(
        [dBP_sNO_df3, dBP_lat_df1, dBP_lon_df2, dBP_cNO_df4, dBP_dofb_df5, dBP_age_df6, dBP_dOfpbd_df7, dBP_dOfnbd_df8,
         dBP_available_df9, dBP_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_ABP_lat = ABP['Latitude']
    d_ABP_lon = ABP['Longitude']
    d_ABP_sNO = ABP['Serial_No']
    d_ABP_contactNo = ABP['Contact_No']
    d_ABP_DOB = ABP['Date_of_Birth']
    d_ABP_age = ABP['Age']
    d_ABP_DOfPreviousBD = ABP['Date_of_Previous_Blood_Donation']
    d_ABP_DOfNextBD = ABP['Date_of_Next_Blood_Donation']
    d_ABP_availability = ABP['Availability']
    d_ABP_Name = ABP['Full_Name']
    dABP_lat_df1 = pd.DataFrame(d_ABP_lat)
    dABP_lon_df2 = pd.DataFrame(d_ABP_lon)
    dABP_sNO_df3 = pd.DataFrame(d_ABP_sNO)
    dABP_cNO_df4 = pd.DataFrame(d_ABP_contactNo)
    dABP_dofb_df5 = pd.DataFrame(d_ABP_DOB)
    dABP_age_df6 = pd.DataFrame(d_ABP_age)
    dABP_dOfpbd_df7 = pd.DataFrame(d_ABP_DOfPreviousBD)
    dABP_dOfnbd_df8 = pd.DataFrame(d_ABP_DOfNextBD)
    dABP_available_df9 = pd.DataFrame(d_ABP_availability)
    dABP_name_df10 = pd.DataFrame(d_ABP_Name)
    ABP_result = pd.concat(
        [dABP_sNO_df3, dABP_lat_df1, dABP_lon_df2, dABP_cNO_df4, dABP_dofb_df5, dABP_age_df6, dABP_dOfpbd_df7,
         dABP_dOfnbd_df8, dABP_available_df9, dABP_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_OP_lat = OP['Latitude']
    d_OP_lon = OP['Longitude']
    d_OP_sNO = OP['Serial_No']
    d_OP_contactNo = OP['Contact_No']
    d_OP_DOB = OP['Date_of_Birth']
    d_OP_age = OP['Age']
    d_OP_DOfPreviousBD = OP['Date_of_Previous_Blood_Donation']
    d_OP_DOfNextBD = OP['Date_of_Next_Blood_Donation']
    d_OP_availability = OP['Availability']
    d_OP_Name = OP['Full_Name']
    dOP_lat_df1 = pd.DataFrame(d_OP_lat)
    dOP_lon_df2 = pd.DataFrame(d_OP_lon)
    dOP_sNO_df3 = pd.DataFrame(d_OP_sNO)
    dOP_cNO_df4 = pd.DataFrame(d_OP_contactNo)
    dOP_dofb_df5 = pd.DataFrame(d_OP_DOB)
    dOP_age_df6 = pd.DataFrame(d_OP_age)
    dOP_dOfpbd_df7 = pd.DataFrame(d_OP_DOfPreviousBD)
    dOP_dOfnbd_df8 = pd.DataFrame(d_OP_DOfNextBD)
    dOP_available_df9 = pd.DataFrame(d_OP_availability)
    dOP_name_df10 = pd.DataFrame(d_OP_Name)
    OP_result = pd.concat(
        [dOP_sNO_df3, dOP_lat_df1, dOP_lon_df2, dOP_cNO_df4, dOP_dofb_df5, dOP_age_df6, dOP_dOfpbd_df7, dOP_dOfnbd_df8,
         dOP_available_df9, dOP_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_AN_lat = AN['Latitude']
    d_AN_lon = AN['Longitude']
    d_AN_sNO = AN['Serial_No']
    d_AN_contactNo = AN['Contact_No']
    d_AN_DOB = AN['Date_of_Birth']
    d_AN_age = AN['Age']
    d_AN_DOfPreviousBD = AN['Date_of_Previous_Blood_Donation']
    d_AN_DOfNextBD = AN['Date_of_Next_Blood_Donation']
    d_AN_availability = AN['Availability']
    d_AN_Name = AN['Full_Name']
    dAN_lat_df1 = pd.DataFrame(d_AN_lat)
    dAN_lon_df2 = pd.DataFrame(d_AN_lon)
    dAN_sNO_df3 = pd.DataFrame(d_AN_sNO)
    dAN_cNO_df4 = pd.DataFrame(d_AN_contactNo)
    dAN_dofb_df5 = pd.DataFrame(d_AN_DOB)
    dAN_age_df6 = pd.DataFrame(d_AN_age)
    dAN_dOfpbd_df7 = pd.DataFrame(d_AN_DOfPreviousBD)
    dAN_dOfnbd_df8 = pd.DataFrame(d_AN_DOfNextBD)
    dAN_available_df9 = pd.DataFrame(d_AN_availability)
    dAN_name_df10 = pd.DataFrame(d_AN_Name)
    AN_result = pd.concat(
        [dAN_sNO_df3, dAN_lat_df1, dAN_lon_df2, dAN_cNO_df4, dAN_dofb_df5, dAN_age_df6, dAN_dOfpbd_df7, dAN_dOfnbd_df8,
         dAN_available_df9, dAN_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_ABN_lat = ABN['Latitude']
    d_ABN_lon = ABN['Longitude']
    d_ABN_sNO = ABN['Serial_No']
    d_ABN_contactNo = ABN['Contact_No']
    d_ABN_DOB = ABN['Date_of_Birth']
    d_ABN_age = ABN['Age']
    d_ABN_DOfPreviousBD = ABN['Date_of_Previous_Blood_Donation']
    d_ABN_DOfNextBD = ABN['Date_of_Next_Blood_Donation']
    d_ABN_availability = ABN['Availability']
    d_ABN_Name = ABN['Full_Name']
    dABN_lat_df1 = pd.DataFrame(d_ABN_lat)
    dABN_lon_df2 = pd.DataFrame(d_ABN_lon)
    dABN_sNO_df3 = pd.DataFrame(d_ABN_sNO)
    dABN_cNO_df4 = pd.DataFrame(d_ABN_contactNo)
    dABN_dofb_df5 = pd.DataFrame(d_ABN_DOB)
    dABN_age_df6 = pd.DataFrame(d_ABN_age)
    dABN_dOfpbd_df7 = pd.DataFrame(d_ABN_DOfPreviousBD)
    dABN_dOfnbd_df8 = pd.DataFrame(d_ABN_DOfNextBD)
    dABN_available_df9 = pd.DataFrame(d_ABN_availability)
    dABN_name_df10 = pd.DataFrame(d_ABN_Name)
    ABN_result = pd.concat(
        [dABN_sNO_df3, dABN_lat_df1, dABN_lon_df2, dABN_cNO_df4, dABN_dofb_df5, dABN_age_df6, dABN_dOfpbd_df7,
         dABN_dOfnbd_df8, dABN_available_df9, dABN_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_ON_lat = ON['Latitude']
    d_ON_lon = ON['Longitude']
    d_ON_sNO = ON['Serial_No']
    d_ON_contactNo = ON['Contact_No']
    d_ON_DOB = ON['Date_of_Birth']
    d_ON_age = ON['Age']
    d_ON_DOfPreviousBD = ON['Date_of_Previous_Blood_Donation']
    d_ON_DOfNextBD = ON['Date_of_Next_Blood_Donation']
    d_ON_availability = ON['Availability']
    d_ON_Name = ON['Full_Name']
    dON_lat_df1 = pd.DataFrame(d_ON_lat)
    dON_lon_df2 = pd.DataFrame(d_ON_lon)
    dON_sNO_df3 = pd.DataFrame(d_ON_sNO)
    dON_cNO_df4 = pd.DataFrame(d_ON_contactNo)
    dON_dofb_df5 = pd.DataFrame(d_ON_DOB)
    dON_age_df6 = pd.DataFrame(d_ON_age)
    dON_dOfpbd_df7 = pd.DataFrame(d_ON_DOfPreviousBD)
    dON_dOfnbd_df8 = pd.DataFrame(d_ON_DOfNextBD)
    dON_available_df9 = pd.DataFrame(d_ON_availability)
    dON_name_df10 = pd.DataFrame(d_ON_Name)
    ON_result = pd.concat(
        [dON_sNO_df3, dON_lat_df1, dON_lon_df2, dON_cNO_df4, dON_dofb_df5, dON_age_df6, dON_dOfpbd_df7, dON_dOfnbd_df8,
         dON_available_df9, dON_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    d_BN_lat = BN['Latitude']
    d_BN_lon = BN['Longitude']
    d_BN_sNO = BN['Serial_No']
    d_BN_contactNo = BN['Contact_No']
    d_BN_DOB = BN['Date_of_Birth']
    d_BN_age = BN['Age']
    d_BN_DOfPreviousBD = BN['Date_of_Previous_Blood_Donation']
    d_BN_DOfNextBD = BN['Date_of_Next_Blood_Donation']
    d_BN_availability = BN['Availability']
    d_BN_Name = BN['Full_Name']
    dBN_lat_df1 = pd.DataFrame(d_BN_lat)
    dBN_lon_df2 = pd.DataFrame(d_BN_lon)
    dBN_sNO_df3 = pd.DataFrame(d_BN_sNO)
    dBN_cNO_df4 = pd.DataFrame(d_BN_contactNo)
    dBN_dofb_df5 = pd.DataFrame(d_BN_DOB)
    dBN_age_df6 = pd.DataFrame(d_BN_age)
    dBN_dOfpbd_df7 = pd.DataFrame(d_BN_DOfPreviousBD)
    dBN_dOfnbd_df8 = pd.DataFrame(d_BN_DOfNextBD)
    dBN_available_df9 = pd.DataFrame(d_BN_availability)
    dBN_name_df10 = pd.DataFrame(d_BN_Name)
    BN_result = pd.concat(
        [dBN_sNO_df3, dBN_lat_df1, dBN_lon_df2, dBN_cNO_df4, dBN_dofb_df5, dBN_age_df6, dBN_dOfpbd_df7, dBN_dOfnbd_df8,
         dBN_available_df9, dBN_name_df10], axis=1, ignore_index=False, sort=False).reset_index()

    # print(ABN_result)


    # ///////////////////////////////////////////////////////////////////////// Create data frame for use in condition and get output

    DONORRESULT_BloodType = pd.DataFrame(columns=['Serial_No', 'Latitude', 'Longitude', 'Contact_No', 'Age', 'Date_of_Next_Blood_Donation',
                            'Availability'])

    #///////////////////////////////////////////////////////////////// Create data frame for check availability

    Available_DONORRESULT_BloodType = pd.DataFrame(columns=['Serial_No', 'Latitude', 'Longitude', 'Contact_No'])


    # //////////////////////////////////////////////////////////////////// Create data frame for get distances between donors and the hospital

    Distance_KM = pd.DataFrame(columns=['Serial_No', 'Distance', 'Contact_No'])

    #https://best-donor.herokuapp.com/bestDonor?latitude=79.878978&longitude=6.922656&stage=1&Blood_Group=AP

