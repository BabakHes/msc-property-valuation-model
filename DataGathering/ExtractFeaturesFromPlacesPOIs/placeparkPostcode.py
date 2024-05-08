import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'park_rating_mean_1500', 'park_rating_std_1500',
    'park_count_1500','park_rating_mean_1000', 'park_rating_std_1000',
    'park_count_1000','park_rating_mean_500', 'park_rating_std_500',
    'park_count_500', 'park_min'
    ]

fileDataCSV = open('postcodeparkData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

parkData = pd.read_csv('ListOfIDs_park.csv')

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
    
    parkData['dist'] = parkData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    park = parkData[parkData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    park_min = park['dist'].min()

    park_rating_mean_1500 = park['rating'].mean()
    park_rating_std_1500 = park['rating'].std()
    park_count_1500 = len(park)

    park = park[park[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    park_rating_mean_1000 = park['rating'].mean()
    park_rating_std_1000 = park['rating'].std()
    park_count_1000 = len(park)

    park = park[park[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    park_rating_mean_500 = park['rating'].mean()
    park_rating_std_500 = park['rating'].std()
    park_count_500 = len(park)

    if math.isnan(park_rating_mean_1500):
        park_rating_mean_1500 = 0.0
    if math.isnan(park_rating_std_1500):
        park_rating_std_1500 = 0.0
    if math.isnan(park_rating_mean_1500):
        park_rating_mean_1500 = 0.0

    if math.isnan(park_rating_mean_1000):
        park_rating_mean_1000 = 0.0
    if math.isnan(park_rating_std_1000):
        park_rating_std_1000 = 0.0
    if math.isnan(park_rating_mean_1000):
        park_rating_mean_1000 = 0.0

    if math.isnan(park_rating_mean_500):
        park_rating_mean_500 = 0.0
    if math.isnan(park_rating_std_500):
        park_rating_std_500 = 0.0
    if math.isnan(park_rating_mean_500):
        park_rating_mean_500 = 0.0


    record = [code, park_rating_mean_1500, park_rating_std_1500,
    park_count_1500,park_rating_mean_1000, park_rating_std_1000,
    park_count_1000,park_rating_mean_500, park_rating_std_500,
    park_count_500, park_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

