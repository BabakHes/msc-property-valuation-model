import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'hindu_temple_rating_mean_1500', 'hindu_temple_rating_std_1500',
    'hindu_temple_count_1500','hindu_temple_rating_mean_1000', 'hindu_temple_rating_std_1000',
    'hindu_temple_count_1000','hindu_temple_rating_mean_500', 'hindu_temple_rating_std_500',
    'hindu_temple_count_500', 'hindu_temple_min'
    ]

fileDataCSV = open('postcodehindu_templeData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

hindu_templeData = pd.read_csv('ListOfIDs_hindu_temple.csv')

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
    
    hindu_templeData['dist'] = hindu_templeData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    hindu_temple = hindu_templeData[hindu_templeData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    hindu_temple_min = hindu_temple['dist'].min()

    hindu_temple_rating_mean_1500 = hindu_temple['rating'].mean()
    hindu_temple_rating_std_1500 = hindu_temple['rating'].std()
    hindu_temple_count_1500 = len(hindu_temple)

    hindu_temple = hindu_temple[hindu_temple[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    hindu_temple_rating_mean_1000 = hindu_temple['rating'].mean()
    hindu_temple_rating_std_1000 = hindu_temple['rating'].std()
    hindu_temple_count_1000 = len(hindu_temple)

    hindu_temple = hindu_temple[hindu_temple[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    hindu_temple_rating_mean_500 = hindu_temple['rating'].mean()
    hindu_temple_rating_std_500 = hindu_temple['rating'].std()
    hindu_temple_count_500 = len(hindu_temple)

    if math.isnan(hindu_temple_rating_mean_1500):
        hindu_temple_rating_mean_1500 = 0.0
    if math.isnan(hindu_temple_rating_std_1500):
        hindu_temple_rating_std_1500 = 0.0
    if math.isnan(hindu_temple_rating_mean_1500):
        hindu_temple_rating_mean_1500 = 0.0

    if math.isnan(hindu_temple_rating_mean_1000):
        hindu_temple_rating_mean_1000 = 0.0
    if math.isnan(hindu_temple_rating_std_1000):
        hindu_temple_rating_std_1000 = 0.0
    if math.isnan(hindu_temple_rating_mean_1000):
        hindu_temple_rating_mean_1000 = 0.0

    if math.isnan(hindu_temple_rating_mean_500):
        hindu_temple_rating_mean_500 = 0.0
    if math.isnan(hindu_temple_rating_std_500):
        hindu_temple_rating_std_500 = 0.0
    if math.isnan(hindu_temple_rating_mean_500):
        hindu_temple_rating_mean_500 = 0.0


    record = [code, hindu_temple_rating_mean_1500, hindu_temple_rating_std_1500,
    hindu_temple_count_1500,hindu_temple_rating_mean_1000, hindu_temple_rating_std_1000,
    hindu_temple_count_1000,hindu_temple_rating_mean_500, hindu_temple_rating_std_500,
    hindu_temple_count_500, hindu_temple_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

