import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'shopping_mall_rating_mean_1500', 'shopping_mall_rating_std_1500',
    'shopping_mall_count_1500','shopping_mall_rating_mean_1000', 'shopping_mall_rating_std_1000',
    'shopping_mall_count_1000','shopping_mall_rating_mean_500', 'shopping_mall_rating_std_500',
    'shopping_mall_count_500', 'shopping_mall_min'
    ]

fileDataCSV = open('postcodeshopping_mallData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

shopping_mallData = pd.read_csv('ListOfIDs_shopping_mall.csv')

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
    
    shopping_mallData['dist'] = shopping_mallData[['lat','lng']].apply(lambda x: dist(x['lat'],x['lng']),axis=1)
    
    shopping_mall = shopping_mallData[shopping_mallData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    shopping_mall_min = shopping_mall['dist'].min()

    shopping_mall_rating_mean_1500 = shopping_mall['rating'].mean()
    shopping_mall_rating_std_1500 = shopping_mall['rating'].std()
    shopping_mall_count_1500 = len(shopping_mall)

    shopping_mall = shopping_mall[shopping_mall[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    shopping_mall_rating_mean_1000 = shopping_mall['rating'].mean()
    shopping_mall_rating_std_1000 = shopping_mall['rating'].std()
    shopping_mall_count_1000 = len(shopping_mall)

    shopping_mall = shopping_mall[shopping_mall[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    shopping_mall_rating_mean_500 = shopping_mall['rating'].mean()
    shopping_mall_rating_std_500 = shopping_mall['rating'].std()
    shopping_mall_count_500 = len(shopping_mall)

    if math.isnan(shopping_mall_rating_mean_1500):
        shopping_mall_rating_mean_1500 = 0.0
    if math.isnan(shopping_mall_rating_std_1500):
        shopping_mall_rating_std_1500 = 0.0
    if math.isnan(shopping_mall_rating_mean_1500):
        shopping_mall_rating_mean_1500 = 0.0

    if math.isnan(shopping_mall_rating_mean_1000):
        shopping_mall_rating_mean_1000 = 0.0
    if math.isnan(shopping_mall_rating_std_1000):
        shopping_mall_rating_std_1000 = 0.0
    if math.isnan(shopping_mall_rating_mean_1000):
        shopping_mall_rating_mean_1000 = 0.0

    if math.isnan(shopping_mall_rating_mean_500):
        shopping_mall_rating_mean_500 = 0.0
    if math.isnan(shopping_mall_rating_std_500):
        shopping_mall_rating_std_500 = 0.0
    if math.isnan(shopping_mall_rating_mean_500):
        shopping_mall_rating_mean_500 = 0.0


    record = [code, shopping_mall_rating_mean_1500, shopping_mall_rating_std_1500,
    shopping_mall_count_1500,shopping_mall_rating_mean_1000, shopping_mall_rating_std_1000,
    shopping_mall_count_1000,shopping_mall_rating_mean_500, shopping_mall_rating_std_500,
    shopping_mall_count_500, shopping_mall_min
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

