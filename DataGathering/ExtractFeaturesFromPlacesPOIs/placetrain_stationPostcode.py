import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'train_station_rating_mean_1500', 'train_station_rating_std_1500',
    'train_station_count_1500','train_station_rating_mean_1000', 'train_station_rating_std_1000',
    'train_station_count_1000','train_station_rating_mean_500', 'train_station_rating_std_500',
    'train_station_count_500', 'train_station_min'
    ]

fileDataCSV = open('postcodetrain_stationData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

train_stationData = pd.read_csv('ListOfIDs_train_station.csv')

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
    
    train_stationData['dist'] = train_stationData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    train_station = train_stationData[train_stationData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    train_station_min = train_station['dist'].min()

    train_station_rating_mean_1500 = train_station['rating'].mean()
    train_station_rating_std_1500 = train_station['rating'].std()
    train_station_count_1500 = len(train_station)

    train_station = train_station[train_station[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    train_station_rating_mean_1000 = train_station['rating'].mean()
    train_station_rating_std_1000 = train_station['rating'].std()
    train_station_count_1000 = len(train_station)

    train_station = train_station[train_station[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    train_station_rating_mean_500 = train_station['rating'].mean()
    train_station_rating_std_500 = train_station['rating'].std()
    train_station_count_500 = len(train_station)

    if math.isnan(train_station_rating_mean_1500):
        train_station_rating_mean_1500 = 0.0
    if math.isnan(train_station_rating_std_1500):
        train_station_rating_std_1500 = 0.0
    if math.isnan(train_station_rating_mean_1500):
        train_station_rating_mean_1500 = 0.0

    if math.isnan(train_station_rating_mean_1000):
        train_station_rating_mean_1000 = 0.0
    if math.isnan(train_station_rating_std_1000):
        train_station_rating_std_1000 = 0.0
    if math.isnan(train_station_rating_mean_1000):
        train_station_rating_mean_1000 = 0.0

    if math.isnan(train_station_rating_mean_500):
        train_station_rating_mean_500 = 0.0
    if math.isnan(train_station_rating_std_500):
        train_station_rating_std_500 = 0.0
    if math.isnan(train_station_rating_mean_500):
        train_station_rating_mean_500 = 0.0


    record = [code, train_station_rating_mean_1500, train_station_rating_std_1500,
    train_station_count_1500,train_station_rating_mean_1000, train_station_rating_std_1000,
    train_station_count_1000,train_station_rating_mean_500, train_station_rating_std_500,
    train_station_count_500, train_station_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

