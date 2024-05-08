import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'restaurants_rating_mean_1500', 'restaurants_rating_std_1500',
    'restaurants_price_level_mean_1500', 'restaurants_price_level_std_1500', 
    'restaurants_count_1500','restaurants_rating_mean_1000', 'restaurants_rating_std_1000',
    'restaurants_price_level_mean_1000', 'restaurants_price_level_std_1000', 
    'restaurants_count_1000','restaurants_rating_mean_500', 'restaurants_rating_std_500',
    'restaurants_price_level_mean_500', 'restaurants_price_level_std_500', 
    'restaurants_count_500',
    ]

fileDataCSV = open('postcodeResturantsData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

restaurantsData = pd.read_csv('ListOfIDs_restaurant.csv')

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
    
    restaurants = restaurantsData[restaurantsData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    restaurants_rating_mean_1500 = restaurants['rating'].mean()
    restaurants_rating_std_1500 = restaurants['rating'].std()
    restaurants_price_level_mean_1500 = restaurants['price_level'].mean()
    restaurants_price_level_std_1500 = restaurants['price_level'].std()
    restaurants_count_1500 = len(restaurants)

    restaurants = restaurants[restaurants[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    restaurants_rating_mean_1000 = restaurants['rating'].mean()
    restaurants_rating_std_1000 = restaurants['rating'].std()
    restaurants_price_level_mean_1000 = restaurants['price_level'].mean()
    restaurants_price_level_std_1000 = restaurants['price_level'].std()
    restaurants_count_1000 = len(restaurants)

    restaurants = restaurants[restaurants[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    restaurants_rating_mean_500 = restaurants['rating'].mean()
    restaurants_rating_std_500 = restaurants['rating'].std()
    restaurants_price_level_mean_500 = restaurants['price_level'].mean()
    restaurants_price_level_std_500 = restaurants['price_level'].std()
    restaurants_count_500 = len(restaurants)

    if math.isnan(restaurants_rating_mean_1500):
        restaurants_rating_mean_1500 = 0.0
    if math.isnan(restaurants_rating_std_1500):
        restaurants_rating_std_1500 = 0.0
    if math.isnan(restaurants_rating_mean_1500):
        restaurants_rating_mean_1500 = 0.0
    if math.isnan(restaurants_price_level_mean_1500):
        restaurants_price_level_mean_1500 = 0.0
    if math.isnan(restaurants_price_level_std_1500):
        restaurants_price_level_std_1500 = 0.0

    if math.isnan(restaurants_rating_mean_1000):
        restaurants_rating_mean_1000 = 0.0
    if math.isnan(restaurants_rating_std_1000):
        restaurants_rating_std_1000 = 0.0
    if math.isnan(restaurants_rating_mean_1000):
        restaurants_rating_mean_1000 = 0.0
    if math.isnan(restaurants_price_level_mean_1000):
        restaurants_price_level_mean_1000 = 0.0
    if math.isnan(restaurants_price_level_std_1000):
        restaurants_price_level_std_1000 = 0.0

    if math.isnan(restaurants_rating_mean_500):
        restaurants_rating_mean_500 = 0.0
    if math.isnan(restaurants_rating_std_500):
        restaurants_rating_std_500 = 0.0
    if math.isnan(restaurants_rating_mean_500):
        restaurants_rating_mean_500 = 0.0
    if math.isnan(restaurants_price_level_mean_500):
        restaurants_price_level_mean_500 = 0.0
    if math.isnan(restaurants_price_level_std_500):
        restaurants_price_level_std_500 = 0.0


    record = [code, restaurants_rating_mean_1500, restaurants_rating_std_1500,
    restaurants_price_level_mean_1500, restaurants_price_level_std_1500, 
    restaurants_count_1500,restaurants_rating_mean_1000, restaurants_rating_std_1000,
    restaurants_price_level_mean_1000, restaurants_price_level_std_1000, 
    restaurants_count_1000,restaurants_rating_mean_500, restaurants_rating_std_500,
    restaurants_price_level_mean_500, restaurants_price_level_std_500, 
    restaurants_count_500,
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

