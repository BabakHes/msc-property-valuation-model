import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'secondary_rating_mean_1500', 'secondary_rating_std_1500',
    'secondary_count_1500','secondary_rating_mean_1000', 'secondary_rating_std_1000',
    'secondary_count_1000','secondary_rating_mean_500', 'secondary_rating_std_500',
    'secondary_count_500', 'secondary_min'
    ]

fileDataCSV = open('postcodesecondaryData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

secondaryData = pd.read_csv('ListOfIDs_secondary_school.csv')

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
    
    secondaryData['dist'] = secondaryData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    secondary = secondaryData[secondaryData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    secondary_min = secondary['dist'].min()

    secondary_rating_mean_1500 = secondary['rating'].mean()
    secondary_rating_std_1500 = secondary['rating'].std()
    secondary_count_1500 = len(secondary)

    secondary = secondary[secondary[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    secondary_rating_mean_1000 = secondary['rating'].mean()
    secondary_rating_std_1000 = secondary['rating'].std()
    secondary_count_1000 = len(secondary)

    secondary = secondary[secondary[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    secondary_rating_mean_500 = secondary['rating'].mean()
    secondary_rating_std_500 = secondary['rating'].std()
    secondary_count_500 = len(secondary)

    if math.isnan(secondary_rating_mean_1500):
        secondary_rating_mean_1500 = 0.0
    if math.isnan(secondary_rating_std_1500):
        secondary_rating_std_1500 = 0.0
    if math.isnan(secondary_rating_mean_1500):
        secondary_rating_mean_1500 = 0.0

    if math.isnan(secondary_rating_mean_1000):
        secondary_rating_mean_1000 = 0.0
    if math.isnan(secondary_rating_std_1000):
        secondary_rating_std_1000 = 0.0
    if math.isnan(secondary_rating_mean_1000):
        secondary_rating_mean_1000 = 0.0

    if math.isnan(secondary_rating_mean_500):
        secondary_rating_mean_500 = 0.0
    if math.isnan(secondary_rating_std_500):
        secondary_rating_std_500 = 0.0
    if math.isnan(secondary_rating_mean_500):
        secondary_rating_mean_500 = 0.0


    record = [code, secondary_rating_mean_1500, secondary_rating_std_1500,
    secondary_count_1500,secondary_rating_mean_1000, secondary_rating_std_1000,
    secondary_count_1000,secondary_rating_mean_500, secondary_rating_std_500,
    secondary_count_500, secondary_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

