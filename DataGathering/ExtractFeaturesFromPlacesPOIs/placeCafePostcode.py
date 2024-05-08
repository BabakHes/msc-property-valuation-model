import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'cafe_rating_mean_1500', 'cafe_rating_std_1500',
    'cafe_price_level_mean_1500', 'cafe_price_level_std_1500', 
    'cafe_count_1500','cafe_rating_mean_1000', 'cafe_rating_std_1000',
    'cafe_price_level_mean_1000', 'cafe_price_level_std_1000', 
    'cafe_count_1000','cafe_rating_mean_500', 'cafe_rating_std_500',
    'cafe_price_level_mean_500', 'cafe_price_level_std_500', 
    'cafe_count_500',
    ]

fileDataCSV = open('postcodecafeData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

cafeData = pd.read_csv('ListOfIDs_cafe.csv')

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
    
    cafe = cafeData[cafeData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    cafe_rating_mean_1500 = cafe['rating'].mean()
    cafe_rating_std_1500 = cafe['rating'].std()
    cafe_price_level_mean_1500 = cafe['price_level'].mean()
    cafe_price_level_std_1500 = cafe['price_level'].std()
    cafe_count_1500 = len(cafe)

    cafe = cafe[cafe[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    cafe_rating_mean_1000 = cafe['rating'].mean()
    cafe_rating_std_1000 = cafe['rating'].std()
    cafe_price_level_mean_1000 = cafe['price_level'].mean()
    cafe_price_level_std_1000 = cafe['price_level'].std()
    cafe_count_1000 = len(cafe)

    cafe = cafe[cafe[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    cafe_rating_mean_500 = cafe['rating'].mean()
    cafe_rating_std_500 = cafe['rating'].std()
    cafe_price_level_mean_500 = cafe['price_level'].mean()
    cafe_price_level_std_500 = cafe['price_level'].std()
    cafe_count_500 = len(cafe)

    if math.isnan(cafe_rating_mean_1500):
        cafe_rating_mean_1500 = 0.0
    if math.isnan(cafe_rating_std_1500):
        cafe_rating_std_1500 = 0.0
    if math.isnan(cafe_rating_mean_1500):
        cafe_rating_mean_1500 = 0.0
    if math.isnan(cafe_price_level_mean_1500):
        cafe_price_level_mean_1500 = 0.0
    if math.isnan(cafe_price_level_std_1500):
        cafe_price_level_std_1500 = 0.0

    if math.isnan(cafe_rating_mean_1000):
        cafe_rating_mean_1000 = 0.0
    if math.isnan(cafe_rating_std_1000):
        cafe_rating_std_1000 = 0.0
    if math.isnan(cafe_rating_mean_1000):
        cafe_rating_mean_1000 = 0.0
    if math.isnan(cafe_price_level_mean_1000):
        cafe_price_level_mean_1000 = 0.0
    if math.isnan(cafe_price_level_std_1000):
        cafe_price_level_std_1000 = 0.0

    if math.isnan(cafe_rating_mean_500):
        cafe_rating_mean_500 = 0.0
    if math.isnan(cafe_rating_std_500):
        cafe_rating_std_500 = 0.0
    if math.isnan(cafe_rating_mean_500):
        cafe_rating_mean_500 = 0.0
    if math.isnan(cafe_price_level_mean_500):
        cafe_price_level_mean_500 = 0.0
    if math.isnan(cafe_price_level_std_500):
        cafe_price_level_std_500 = 0.0


    record = [code, cafe_rating_mean_1500, cafe_rating_std_1500,
    cafe_price_level_mean_1500, cafe_price_level_std_1500, 
    cafe_count_1500,cafe_rating_mean_1000, cafe_rating_std_1000,
    cafe_price_level_mean_1000, cafe_price_level_std_1000, 
    cafe_count_1000,cafe_rating_mean_500, cafe_rating_std_500,
    cafe_price_level_mean_500, cafe_price_level_std_500, 
    cafe_count_500,
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

