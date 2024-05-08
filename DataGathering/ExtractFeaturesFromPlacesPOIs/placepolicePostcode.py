import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'police_rating_mean_1500', 'police_rating_std_1500',
    'police_count_1500','police_rating_mean_1000', 'police_rating_std_1000',
    'police_count_1000','police_rating_mean_500', 'police_rating_std_500',
    'police_count_500', 'police_min'
    ]

fileDataCSV = open('postcodepoliceData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

policeData = pd.read_csv('ListOfIDs_police.csv')

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
    
    policeData['dist'] = policeData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    police = policeData[policeData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    police_min = police['dist'].min()

    police_rating_mean_1500 = police['rating'].mean()
    police_rating_std_1500 = police['rating'].std()
    police_count_1500 = len(police)

    police = police[police[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    police_rating_mean_1000 = police['rating'].mean()
    police_rating_std_1000 = police['rating'].std()
    police_count_1000 = len(police)

    police = police[police[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    police_rating_mean_500 = police['rating'].mean()
    police_rating_std_500 = police['rating'].std()
    police_count_500 = len(police)

    if math.isnan(police_rating_mean_1500):
        police_rating_mean_1500 = 0.0
    if math.isnan(police_rating_std_1500):
        police_rating_std_1500 = 0.0
    if math.isnan(police_rating_mean_1500):
        police_rating_mean_1500 = 0.0

    if math.isnan(police_rating_mean_1000):
        police_rating_mean_1000 = 0.0
    if math.isnan(police_rating_std_1000):
        police_rating_std_1000 = 0.0
    if math.isnan(police_rating_mean_1000):
        police_rating_mean_1000 = 0.0

    if math.isnan(police_rating_mean_500):
        police_rating_mean_500 = 0.0
    if math.isnan(police_rating_std_500):
        police_rating_std_500 = 0.0
    if math.isnan(police_rating_mean_500):
        police_rating_mean_500 = 0.0


    record = [code, police_rating_mean_1500, police_rating_std_1500,
    police_count_1500,police_rating_mean_1000, police_rating_std_1000,
    police_count_1000,police_rating_mean_500, police_rating_std_500,
    police_count_500, police_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

