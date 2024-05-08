import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'cemetery_rating_mean_1500', 'cemetery_rating_std_1500',
    'cemetery_count_1500','cemetery_rating_mean_1000', 'cemetery_rating_std_1000',
    'cemetery_count_1000','cemetery_rating_mean_500', 'cemetery_rating_std_500',
    'cemetery_count_500', 'cemetery_min'
    ]

fileDataCSV = open('postcodecemeteryData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

cemeteryData = pd.read_csv('ListOfIDs_cemetery.csv')

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
    
    cemeteryData['dist'] = cemeteryData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    cemetery = cemeteryData[cemeteryData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    cemetery_min = cemetery['dist'].min()

    cemetery_rating_mean_1500 = cemetery['rating'].mean()
    cemetery_rating_std_1500 = cemetery['rating'].std()
    cemetery_count_1500 = len(cemetery)

    cemetery = cemetery[cemetery[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    cemetery_rating_mean_1000 = cemetery['rating'].mean()
    cemetery_rating_std_1000 = cemetery['rating'].std()
    cemetery_count_1000 = len(cemetery)

    cemetery = cemetery[cemetery[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    cemetery_rating_mean_500 = cemetery['rating'].mean()
    cemetery_rating_std_500 = cemetery['rating'].std()
    cemetery_count_500 = len(cemetery)

    if math.isnan(cemetery_rating_mean_1500):
        cemetery_rating_mean_1500 = 0.0
    if math.isnan(cemetery_rating_std_1500):
        cemetery_rating_std_1500 = 0.0
    if math.isnan(cemetery_rating_mean_1500):
        cemetery_rating_mean_1500 = 0.0

    if math.isnan(cemetery_rating_mean_1000):
        cemetery_rating_mean_1000 = 0.0
    if math.isnan(cemetery_rating_std_1000):
        cemetery_rating_std_1000 = 0.0
    if math.isnan(cemetery_rating_mean_1000):
        cemetery_rating_mean_1000 = 0.0

    if math.isnan(cemetery_rating_mean_500):
        cemetery_rating_mean_500 = 0.0
    if math.isnan(cemetery_rating_std_500):
        cemetery_rating_std_500 = 0.0
    if math.isnan(cemetery_rating_mean_500):
        cemetery_rating_mean_500 = 0.0


    record = [code, cemetery_rating_mean_1500, cemetery_rating_std_1500,
    cemetery_count_1500,cemetery_rating_mean_1000, cemetery_rating_std_1000,
    cemetery_count_1000,cemetery_rating_mean_500, cemetery_rating_std_500,
    cemetery_count_500, cemetery_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

