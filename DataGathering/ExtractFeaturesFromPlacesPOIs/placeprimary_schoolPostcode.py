import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'primary_rating_mean_1500', 'primary_rating_std_1500',
    'primary_count_1500','primary_rating_mean_1000', 'primary_rating_std_1000',
    'primary_count_1000','primary_rating_mean_500', 'primary_rating_std_500',
    'primary_count_500', 'primary_min'
    ]

fileDataCSV = open('postcodeprimaryData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

primaryData = pd.read_csv('ListOfIDs_primary_school.csv')

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
    
    primaryData['dist'] = primaryData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    primary = primaryData[primaryData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    primary_min = primary['dist'].min()

    primary_rating_mean_1500 = primary['rating'].mean()
    primary_rating_std_1500 = primary['rating'].std()
    primary_count_1500 = len(primary)

    primary = primary[primary[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    primary_rating_mean_1000 = primary['rating'].mean()
    primary_rating_std_1000 = primary['rating'].std()
    primary_count_1000 = len(primary)

    primary = primary[primary[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    primary_rating_mean_500 = primary['rating'].mean()
    primary_rating_std_500 = primary['rating'].std()
    primary_count_500 = len(primary)

    if math.isnan(primary_rating_mean_1500):
        primary_rating_mean_1500 = 0.0
    if math.isnan(primary_rating_std_1500):
        primary_rating_std_1500 = 0.0
    if math.isnan(primary_rating_mean_1500):
        primary_rating_mean_1500 = 0.0

    if math.isnan(primary_rating_mean_1000):
        primary_rating_mean_1000 = 0.0
    if math.isnan(primary_rating_std_1000):
        primary_rating_std_1000 = 0.0
    if math.isnan(primary_rating_mean_1000):
        primary_rating_mean_1000 = 0.0

    if math.isnan(primary_rating_mean_500):
        primary_rating_mean_500 = 0.0
    if math.isnan(primary_rating_std_500):
        primary_rating_std_500 = 0.0
    if math.isnan(primary_rating_mean_500):
        primary_rating_mean_500 = 0.0


    record = [code, primary_rating_mean_1500, primary_rating_std_1500,
    primary_count_1500,primary_rating_mean_1000, primary_rating_std_1000,
    primary_count_1000,primary_rating_mean_500, primary_rating_std_500,
    primary_count_500, primary_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

