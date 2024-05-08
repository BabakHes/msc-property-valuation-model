import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'mosque_rating_mean_1500', 'mosque_rating_std_1500',
    'mosque_count_1500','mosque_rating_mean_1000', 'mosque_rating_std_1000',
    'mosque_count_1000','mosque_rating_mean_500', 'mosque_rating_std_500',
    'mosque_count_500', 'mosque_min'
    ]

fileDataCSV = open('postcodemosqueData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

mosqueData = pd.read_csv('ListOfIDs_mosque.csv')

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
    
    mosqueData['dist'] = mosqueData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    mosque = mosqueData[mosqueData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    mosque_min = mosque['dist'].min()

    mosque_rating_mean_1500 = mosque['rating'].mean()
    mosque_rating_std_1500 = mosque['rating'].std()
    mosque_count_1500 = len(mosque)

    mosque = mosque[mosque[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    mosque_rating_mean_1000 = mosque['rating'].mean()
    mosque_rating_std_1000 = mosque['rating'].std()
    mosque_count_1000 = len(mosque)

    mosque = mosque[mosque[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    mosque_rating_mean_500 = mosque['rating'].mean()
    mosque_rating_std_500 = mosque['rating'].std()
    mosque_count_500 = len(mosque)

    if math.isnan(mosque_rating_mean_1500):
        mosque_rating_mean_1500 = 0.0
    if math.isnan(mosque_rating_std_1500):
        mosque_rating_std_1500 = 0.0
    if math.isnan(mosque_rating_mean_1500):
        mosque_rating_mean_1500 = 0.0

    if math.isnan(mosque_rating_mean_1000):
        mosque_rating_mean_1000 = 0.0
    if math.isnan(mosque_rating_std_1000):
        mosque_rating_std_1000 = 0.0
    if math.isnan(mosque_rating_mean_1000):
        mosque_rating_mean_1000 = 0.0

    if math.isnan(mosque_rating_mean_500):
        mosque_rating_mean_500 = 0.0
    if math.isnan(mosque_rating_std_500):
        mosque_rating_std_500 = 0.0
    if math.isnan(mosque_rating_mean_500):
        mosque_rating_mean_500 = 0.0


    record = [code, mosque_rating_mean_1500, mosque_rating_std_1500,
    mosque_count_1500,mosque_rating_mean_1000, mosque_rating_std_1000,
    mosque_count_1000,mosque_rating_mean_500, mosque_rating_std_500,
    mosque_count_500, mosque_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

