import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'fire_station_rating_mean_1500', 'fire_station_rating_std_1500',
    'fire_station_count_1500','fire_station_rating_mean_1000', 'fire_station_rating_std_1000',
    'fire_station_count_1000','fire_station_rating_mean_500', 'fire_station_rating_std_500',
    'fire_station_count_500', 'fire_station_min'
    ]

fileDataCSV = open('postcodefire_stationData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

fire_stationData = pd.read_csv('ListOfIDs_fire_station.csv')

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
    
    fire_stationData['dist'] = fire_stationData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    fire_station = fire_stationData[fire_stationData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    fire_station_min = fire_station['dist'].min()

    fire_station_rating_mean_1500 = fire_station['rating'].mean()
    fire_station_rating_std_1500 = fire_station['rating'].std()
    fire_station_count_1500 = len(fire_station)

    fire_station = fire_station[fire_station[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    fire_station_rating_mean_1000 = fire_station['rating'].mean()
    fire_station_rating_std_1000 = fire_station['rating'].std()
    fire_station_count_1000 = len(fire_station)

    fire_station = fire_station[fire_station[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    fire_station_rating_mean_500 = fire_station['rating'].mean()
    fire_station_rating_std_500 = fire_station['rating'].std()
    fire_station_count_500 = len(fire_station)

    if math.isnan(fire_station_rating_mean_1500):
        fire_station_rating_mean_1500 = 0.0
    if math.isnan(fire_station_rating_std_1500):
        fire_station_rating_std_1500 = 0.0
    if math.isnan(fire_station_rating_mean_1500):
        fire_station_rating_mean_1500 = 0.0

    if math.isnan(fire_station_rating_mean_1000):
        fire_station_rating_mean_1000 = 0.0
    if math.isnan(fire_station_rating_std_1000):
        fire_station_rating_std_1000 = 0.0
    if math.isnan(fire_station_rating_mean_1000):
        fire_station_rating_mean_1000 = 0.0

    if math.isnan(fire_station_rating_mean_500):
        fire_station_rating_mean_500 = 0.0
    if math.isnan(fire_station_rating_std_500):
        fire_station_rating_std_500 = 0.0
    if math.isnan(fire_station_rating_mean_500):
        fire_station_rating_mean_500 = 0.0


    record = [code, fire_station_rating_mean_1500, fire_station_rating_std_1500,
    fire_station_count_1500,fire_station_rating_mean_1000, fire_station_rating_std_1000,
    fire_station_count_1000,fire_station_rating_mean_500, fire_station_rating_std_500,
    fire_station_count_500, fire_station_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

