import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'bars_rating_mean_1500', 'bars_rating_std_1500',
    'bars_price_level_mean_1500', 'bars_price_level_std_1500', 
    'bars_count_1500','bars_rating_mean_1000', 'bars_rating_std_1000',
    'bars_price_level_mean_1000', 'bars_price_level_std_1000', 
    'bars_count_1000','bars_rating_mean_500', 'bars_rating_std_500',
    'bars_price_level_mean_500', 'bars_price_level_std_500', 
    'bars_count_500',
    ]

fileDataCSV = open('postcodeBarsData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

barsData = pd.read_csv('ListOfIDs_bar.csv')

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
    
    bars = barsData[barsData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    bars_rating_mean_1500 = bars['rating'].mean()
    bars_rating_std_1500 = bars['rating'].std()
    bars_price_level_mean_1500 = bars['price_level'].mean()
    bars_price_level_std_1500 = bars['price_level'].std()
    bars_count_1500 = len(bars)

    bars = bars[bars[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    bars_rating_mean_1000 = bars['rating'].mean()
    bars_rating_std_1000 = bars['rating'].std()
    bars_price_level_mean_1000 = bars['price_level'].mean()
    bars_price_level_std_1000 = bars['price_level'].std()
    bars_count_1000 = len(bars)

    bars = bars[bars[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    bars_rating_mean_500 = bars['rating'].mean()
    bars_rating_std_500 = bars['rating'].std()
    bars_price_level_mean_500 = bars['price_level'].mean()
    bars_price_level_std_500 = bars['price_level'].std()
    bars_count_500 = len(bars)

    if math.isnan(bars_rating_mean_1500):
        bars_rating_mean_1500 = 0.0
    if math.isnan(bars_rating_std_1500):
        bars_rating_std_1500 = 0.0
    if math.isnan(bars_rating_mean_1500):
        bars_rating_mean_1500 = 0.0
    if math.isnan(bars_price_level_mean_1500):
        bars_price_level_mean_1500 = 0.0
    if math.isnan(bars_price_level_std_1500):
        bars_price_level_std_1500 = 0.0

    if math.isnan(bars_rating_mean_1000):
        bars_rating_mean_1000 = 0.0
    if math.isnan(bars_rating_std_1000):
        bars_rating_std_1000 = 0.0
    if math.isnan(bars_rating_mean_1000):
        bars_rating_mean_1000 = 0.0
    if math.isnan(bars_price_level_mean_1000):
        bars_price_level_mean_1000 = 0.0
    if math.isnan(bars_price_level_std_1000):
        bars_price_level_std_1000 = 0.0

    if math.isnan(bars_rating_mean_500):
        bars_rating_mean_500 = 0.0
    if math.isnan(bars_rating_std_500):
        bars_rating_std_500 = 0.0
    if math.isnan(bars_rating_mean_500):
        bars_rating_mean_500 = 0.0
    if math.isnan(bars_price_level_mean_500):
        bars_price_level_mean_500 = 0.0
    if math.isnan(bars_price_level_std_500):
        bars_price_level_std_500 = 0.0


    record = [code, bars_rating_mean_1500, bars_rating_std_1500,
    bars_price_level_mean_1500, bars_price_level_std_1500, 
    bars_count_1500,bars_rating_mean_1000, bars_rating_std_1000,
    bars_price_level_mean_1000, bars_price_level_std_1000, 
    bars_count_1000,bars_rating_mean_500, bars_rating_std_500,
    bars_price_level_mean_500, bars_price_level_std_500, 
    bars_count_500,
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

