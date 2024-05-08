import haversine as hs

from datetime import datetime
import pickle
import pandas as pd
import csv
import time
import math

fields = ['code', 'university_rating_mean_1500', 'university_rating_std_1500',
    'university_count_1500','university_rating_mean_1000', 'university_rating_std_1000',
    'university_count_1000','university_rating_mean_500', 'university_rating_std_500',
    'university_count_500',
    ]

fileDataCSV = open('postcodeuniversityData.csv', 'w')
csvDatawriter = csv.writer(fileDataCSV)
csvDatawriter.writerow(fields)

postCodeData = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')

postCodeData = postCodeData[postCodeData['District']=='Lambeth'].copy()

postCodeData.drop_duplicates(subset=['Postcode'], keep='last',inplace=True)

universityData = pd.read_csv('ListOfIDs_university.csv')

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
    
    university = universityData[universityData[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.5),axis=1)].copy()

    university_rating_mean_1500 = university['rating'].mean()
    university_rating_std_1500 = university['rating'].std()
    university_count_1500 = len(university)

    university = university[university[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],1.0),axis=1)].copy()

    university_rating_mean_1000 = university['rating'].mean()
    university_rating_std_1000 = university['rating'].std()
    university_count_1000 = len(university)

    university = university[university[['lat','lng']].apply(lambda x: near(x['lat'],x['lng'],0.5),axis=1)].copy()

    university_rating_mean_500 = university['rating'].mean()
    university_rating_std_500 = university['rating'].std()
    university_count_500 = len(university)

    if math.isnan(university_rating_mean_1500):
        university_rating_mean_1500 = 0.0
    if math.isnan(university_rating_std_1500):
        university_rating_std_1500 = 0.0
    if math.isnan(university_rating_mean_1500):
        university_rating_mean_1500 = 0.0

    if math.isnan(university_rating_mean_1000):
        university_rating_mean_1000 = 0.0
    if math.isnan(university_rating_std_1000):
        university_rating_std_1000 = 0.0
    if math.isnan(university_rating_mean_1000):
        university_rating_mean_1000 = 0.0

    if math.isnan(university_rating_mean_500):
        university_rating_mean_500 = 0.0
    if math.isnan(university_rating_std_500):
        university_rating_std_500 = 0.0
    if math.isnan(university_rating_mean_500):
        university_rating_mean_500 = 0.0


    record = [code, university_rating_mean_1500, university_rating_std_1500,
    university_count_1500,university_rating_mean_1000, university_rating_std_1000,
    university_count_1000,university_rating_mean_500, university_rating_std_500,
    university_count_500,
    ]
    csvDatawriter.writerow(record)


fileDataCSV.close() 

