import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'parking_rating_mean_1500', 'parking_rating_std_1500',
    'parking_count_1500','parking_rating_mean_1000', 'parking_rating_std_1000',
    'parking_count_1000','parking_rating_mean_500', 'parking_rating_std_500',
    'parking_count_500', 'parking_min'
    ]

fileDataCSV = open('postcodeparkingData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

parkingData = pd.read_csv('ListOfIDs_parking.csv')

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
    
    parkingData['dist'] = parkingData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    parking = parkingData[parkingData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    parking_min = parking['dist'].min()

    parking_rating_mean_1500 = parking['rating'].mean()
    parking_rating_std_1500 = parking['rating'].std()
    parking_count_1500 = len(parking)

    parking = parking[parking[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    parking_rating_mean_1000 = parking['rating'].mean()
    parking_rating_std_1000 = parking['rating'].std()
    parking_count_1000 = len(parking)

    parking = parking[parking[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    parking_rating_mean_500 = parking['rating'].mean()
    parking_rating_std_500 = parking['rating'].std()
    parking_count_500 = len(parking)

    if math.isnan(parking_rating_mean_1500):
        parking_rating_mean_1500 = 0.0
    if math.isnan(parking_rating_std_1500):
        parking_rating_std_1500 = 0.0
    if math.isnan(parking_rating_mean_1500):
        parking_rating_mean_1500 = 0.0

    if math.isnan(parking_rating_mean_1000):
        parking_rating_mean_1000 = 0.0
    if math.isnan(parking_rating_std_1000):
        parking_rating_std_1000 = 0.0
    if math.isnan(parking_rating_mean_1000):
        parking_rating_mean_1000 = 0.0

    if math.isnan(parking_rating_mean_500):
        parking_rating_mean_500 = 0.0
    if math.isnan(parking_rating_std_500):
        parking_rating_std_500 = 0.0
    if math.isnan(parking_rating_mean_500):
        parking_rating_mean_500 = 0.0


    record = [code, parking_rating_mean_1500, parking_rating_std_1500,
    parking_count_1500,parking_rating_mean_1000, parking_rating_std_1000,
    parking_count_1000,parking_rating_mean_500, parking_rating_std_500,
    parking_count_500, parking_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

