import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'hospital_rating_mean_1500', 'hospital_rating_std_1500',
    'hospital_count_1500','hospital_rating_mean_1000', 'hospital_rating_std_1000',
    'hospital_count_1000','hospital_rating_mean_500', 'hospital_rating_std_500',
    'hospital_count_500', 'hospital_min'
    ]

fileDataCSV = open('postcodehospitalData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

hospitalData = pd.read_csv('ListOfIDs_hospital.csv')

count = 0
for idx in range(len(postCodeData)):
    reg = postCodeData.iloc[idx]
    code = reg['Postcode']
    lat = reg['Latitude']
    lng = reg['Longitude']

    print(code)

    def near(latP,lagP,POST_CODE_DISTANCE):
        loc1 = (latP,lagP)
        loc2 = (lat,lng)

        dist = hs.haversine(loc1,loc2)
        
        return dist < POST_CODE_DISTANCE
    
    def dist(latP,lagP):
        loc1 = (latP,lagP)
        loc2 = (lat,lng)

        dist = hs.haversine(loc1,loc2)
        
        return dist
    
    hospitalData['dist'] = hospitalData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    hospital = hospitalData[hospitalData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    

    hospital_min = hospital['dist'].min()

    hospital_rating_mean_1500 = hospital['rating'].mean()
    hospital_rating_std_1500 = hospital['rating'].std()
    hospital_count_1500 = len(hospital)

    hospital = hospital[hospital[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    hospital_rating_mean_1000 = hospital['rating'].mean()
    hospital_rating_std_1000 = hospital['rating'].std()
    hospital_count_1000 = len(hospital)

    hospital = hospital[hospital[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    hospital_rating_mean_500 = hospital['rating'].mean()
    hospital_rating_std_500 = hospital['rating'].std()
    hospital_count_500 = len(hospital)

    if math.isnan(hospital_rating_mean_1500):
        hospital_rating_mean_1500 = 0.0
    if math.isnan(hospital_rating_std_1500):
        hospital_rating_std_1500 = 0.0
    if math.isnan(hospital_rating_mean_1500):
        hospital_rating_mean_1500 = 0.0

    if math.isnan(hospital_rating_mean_1000):
        hospital_rating_mean_1000 = 0.0
    if math.isnan(hospital_rating_std_1000):
        hospital_rating_std_1000 = 0.0
    if math.isnan(hospital_rating_mean_1000):
        hospital_rating_mean_1000 = 0.0

    if math.isnan(hospital_rating_mean_500):
        hospital_rating_mean_500 = 0.0
    if math.isnan(hospital_rating_std_500):
        hospital_rating_std_500 = 0.0
    if math.isnan(hospital_rating_mean_500):
        hospital_rating_mean_500 = 0.0


    record = [code, hospital_rating_mean_1500, hospital_rating_std_1500,
    hospital_count_1500,hospital_rating_mean_1000, hospital_rating_std_1000,
    hospital_count_1000,hospital_rating_mean_500, hospital_rating_std_500,
    hospital_count_500, hospital_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

