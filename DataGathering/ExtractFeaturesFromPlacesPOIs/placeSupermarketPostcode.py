import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'supermarket_rating_mean_1500', 'supermarket_rating_std_1500',
    'supermarket_price_level_mean_1500', 'supermarket_price_level_std_1500', 
    'supermarket_count_1500','supermarket_rating_mean_1000', 'supermarket_rating_std_1000',
    'supermarket_price_level_mean_1000', 'supermarket_price_level_std_1000', 
    'supermarket_count_1000','supermarket_rating_mean_500', 'supermarket_rating_std_500',
    'supermarket_price_level_mean_500', 'supermarket_price_level_std_500', 
    'supermarket_count_500',
    ]

fileDataCSV = open('postcodesupermarketData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

supermarketData = pd.read_csv('ListOfIDs_supermarket.csv')

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
    
    supermarket = supermarketData[supermarketData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    supermarket_rating_mean_1500 = supermarket['rating'].mean()
    supermarket_rating_std_1500 = supermarket['rating'].std()
    supermarket_price_level_mean_1500 = supermarket['price_level'].mean()
    supermarket_price_level_std_1500 = supermarket['price_level'].std()
    supermarket_count_1500 = len(supermarket)

    supermarket = supermarket[supermarket[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    supermarket_rating_mean_1000 = supermarket['rating'].mean()
    supermarket_rating_std_1000 = supermarket['rating'].std()
    supermarket_price_level_mean_1000 = supermarket['price_level'].mean()
    supermarket_price_level_std_1000 = supermarket['price_level'].std()
    supermarket_count_1000 = len(supermarket)

    supermarket = supermarket[supermarket[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    supermarket_rating_mean_500 = supermarket['rating'].mean()
    supermarket_rating_std_500 = supermarket['rating'].std()
    supermarket_price_level_mean_500 = supermarket['price_level'].mean()
    supermarket_price_level_std_500 = supermarket['price_level'].std()
    supermarket_count_500 = len(supermarket)

    if math.isnan(supermarket_rating_mean_1500):
        supermarket_rating_mean_1500 = 0.0
    if math.isnan(supermarket_rating_std_1500):
        supermarket_rating_std_1500 = 0.0
    if math.isnan(supermarket_rating_mean_1500):
        supermarket_rating_mean_1500 = 0.0
    if math.isnan(supermarket_price_level_mean_1500):
        supermarket_price_level_mean_1500 = 0.0
    if math.isnan(supermarket_price_level_std_1500):
        supermarket_price_level_std_1500 = 0.0

    if math.isnan(supermarket_rating_mean_1000):
        supermarket_rating_mean_1000 = 0.0
    if math.isnan(supermarket_rating_std_1000):
        supermarket_rating_std_1000 = 0.0
    if math.isnan(supermarket_rating_mean_1000):
        supermarket_rating_mean_1000 = 0.0
    if math.isnan(supermarket_price_level_mean_1000):
        supermarket_price_level_mean_1000 = 0.0
    if math.isnan(supermarket_price_level_std_1000):
        supermarket_price_level_std_1000 = 0.0

    if math.isnan(supermarket_rating_mean_500):
        supermarket_rating_mean_500 = 0.0
    if math.isnan(supermarket_rating_std_500):
        supermarket_rating_std_500 = 0.0
    if math.isnan(supermarket_rating_mean_500):
        supermarket_rating_mean_500 = 0.0
    if math.isnan(supermarket_price_level_mean_500):
        supermarket_price_level_mean_500 = 0.0
    if math.isnan(supermarket_price_level_std_500):
        supermarket_price_level_std_500 = 0.0


    record = [code, supermarket_rating_mean_1500, supermarket_rating_std_1500,
    supermarket_price_level_mean_1500, supermarket_price_level_std_1500, 
    supermarket_count_1500,supermarket_rating_mean_1000, supermarket_rating_std_1000,
    supermarket_price_level_mean_1000, supermarket_price_level_std_1000, 
    supermarket_count_1000,supermarket_rating_mean_500, supermarket_rating_std_500,
    supermarket_price_level_mean_500, supermarket_price_level_std_500, 
    supermarket_count_500,
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

