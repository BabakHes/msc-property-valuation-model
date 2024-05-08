import requests

from datetime import datetime
import pickle
import pandas as pd
import csv
import time

# Loads demographic and market dynamics using 3 PropertyData APIs:
#
# /growt
# /crime
# /demographics
#
# uses post codes from: areaCodeData.csv
# Data is saved in: areaCodeData.csv

resetScanning = False
key = "RKDUXQSVR0"
URL = "https://api.propertydata.co.uk/"

fields = [ 'code',
    '2016_Value', '2017_Value', '2017_growth', '2018_Value', '2018_growth', '2019_Value', '2019_growth', '2020_Value','2020_growth',
    'population', 'crimes_last_12m', 'crimes_per_thousand', 'crime_rating', 'PublicOrder',
    'Burglary', 'Robbery', 'PossessionOfWeapons', 'BicycleTheft', 'AntiSocialBehaviour', 'Violence',
    'Theft', 'Shoplifting', 'OtherCrime', 'Drugs', 'OtherTheft', 'VehicleCrime', 'CriminalDamage',
    'deprivation', 'health', 'age0_4', 'age5_9', 'age10_14', 'age15_19', 'age20_24', 'age25_29', 'age30_34', 'age35_39',
    'age40_44', 'age45_49', 'age50_54', 'age55_59', 'age60_64', 'age65_69', 'age70_74', 'age75_79','age80_84', 'age85_89',
    'proportion_with_degree', 'vehicles_per_household', 'commute_method_foot','commute_method_bicycle',
    'commute_method_other', 'commute_method_motorcycle','commute_method_taxi','commute_method_train',
    'commute_method_bus', 'commute_method_underground_light_rail','commute_method_car_driver', 
    'commute_method_at_home', 'commute_method_car_passenger','social_grade_ab', 'social_grade_de',
    'social_grade_c1', 'social_grade_c2']

exist_codes = set()

if resetScanning:

    fileDataCSV = open('areaCodeData.csv', 'w')
    csvDatawriter = csv.writer(fileDataCSV)
    csvDatawriter.writerow(fields)
else:

    exist = pd.read_csv('areaCodeData.csv')
    exist_codes = set(exist['code'])
    del(exist)

    fileDataCSV = open('areaCodeData.csv', 'a+', newline='')
    csvDatawriter = csv.writer(fileDataCSV)


#properties = pd.read_csv('../MergePPCert/UseOnlyPP.csv')
properties = pd.read_csv('postCodeData.csv')

#codes = set(properties['postcode'].apply(lambda x: x.split()[0]))- exist_codes
#codes = set(properties['postcode'])- exist_codes
codes = set(properties['code'])- exist_codes
print(codes)
print(len(codes))

for code in codes:

    print(code)

    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'key': key , "postcode": code}

    endpoint = "growth"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format

    data = r.json()

    print(data)

    if data['status'] == "success":
        growth={}
        count=0
        for item in data['data']:
            growth[count]={}
            year = item[0].split()[1]
            number = item[1]
            if item[2]:
                percen = float(item[2][:-1])
            else:
                percen = None
            growth[count]['year']=year
            growth[count]['number']=number
            growth[count]['percen']=percen
            count+=1
        try:
            Year_1_Value = growth[0]['number']
        except:
            Year_1_Value = 0
        try:
            Year_2_Value = growth[1]['number']
        except:
            Year_2_Value = 0
        try:
            Year_2_growth = growth[1]['percen']
        except:
            Year_2_growth = 0
        try:
            Year_3_Value = growth[2]['number']
        except:
            Year_3_Value = 0
        try:
            Year_3_growth = growth[2]['percen']
        except:
            Year_3_growth = 0
        try:
            Year_4_Value =  growth[3]['number']
        except:
            Year_4_Value = 0
        try:
            Year_4_growth = growth[3]['percen']
        except:
            Year_4_growth = 0
        try:
            Year_5_Value = growth[4]['number']
        except:
            Year_5_Value = 0
        try:
            Year_5_growth = growth[4]['percen']
        except:
            Year_5_growth = 0
    else:
        print(data)
        pass


    endpoint = "crime"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    print(data)

    if data['status'] == "success":
        try:
            population = data['population']
        except:
            population = 0
        try:    
            crimes_last_12m = data['crimes_last_12m']
        except:
            crimes_last_12m = 0
        try:  
            crimes_per_thousand = data['crimes_per_thousand']
        except:
            crimes_per_thousand = 0
        try:  
            crime_rating = data['crime_rating']
        except:
            crime_rating = 0
        try:  
            PublicOrder=data['types']['Public order']
        except:
            PublicOrder = 0
        try:  
            Burglary=data['types']['Burglary']
        except:
            Burglary = 0
        try:  
            Robbery=data['types']['Robbery']
        except:
            Robbery = 0
        try:  
            PossessionOfWeapons=data['types']['Possession of weapons']
        except:
            PossessionOfWeapons = 0
        try:  
            BicycleTheft=data['types']['Bicycle theft']
        except:
            BicycleTheft = 0
        try:  
            AntiSocialBehaviour=data['types']['Anti-social behaviour']
        except:
            AntiSocialBehaviour = 0
        try:  
            Violence=data['types']['Violence and sexual offences']
        except:
            Violence = 0
        try:  
            Theft=data['types']['Theft from the person']
        except:
            Theft = 0
        try:  
            Shoplifting=data['types']['Shoplifting']
        except:
            Shoplifting = 0
        try:  
            OtherCrime=data['types']['Other crime']
        except:
            OtherCrime = 0
        try:  
            Drugs=data['types']['Drugs']
        except:
            Drugs = 0
        try:  
            OtherTheft=data['types']['Other theft']
        except:
            OtherTheft = 0
        try:  
            VehicleCrime=data['types']['Vehicle crime']
        except:
            VehicleCrime = 0
        try:  
            CriminalDamage=data['types']['Criminal damage and arson']
        except:
            CriminalDamage = 0
    else:
        print(data)
        pass


    endpoint = "demographics"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    print(data)


    if data['status'] == "success":
        try:
            deprivation=float(data['data']['deprivation'])
        except:
            deprivation=0
        try:
            health=float(data['data']['health'])
        except:
            health=0
        try:
            age0_4 = float(data['data']['age']['0-4'])
        except:
            age0_4=0
        try:
            age5_9 = float(data['data']['age']['5-9'])
        except:
            age5_9=0
        try:
            age10_14 = float(data['data']['age']['10-14'])
        except:
            age10_14=0
        try:
            age15_19 = float(data['data']['age']['15-19'])
        except:
            age15_19=0
        try:
            age20_24 = float(data['data']['age']['20-24'])
        except:
            age20_24=0
        try:
            age25_29 = float(data['data']['age']['25-29'])
        except:
            age25_29=0
        try:
            age30_34 = float(data['data']['age']['30-34'])
        except:
            age30_34=0
        try:
            age35_39 = float(data['data']['age']['35-39'])
        except:
            age35_39=0
        try:
            age40_44 = float(data['data']['age']['40-44'])
        except:
            age40_44=0
        try:
            age45_49 = float(data['data']['age']['45-49'])
        except:
            age45_49=0
        try:
            age50_54 = float(data['data']['age']['50-54'])
        except:
            age50_54=0
        try:
            age55_59 = float(data['data']['age']['55-59'])
        except:
            age55_59=0
        try:
            age60_64 = float(data['data']['age']['60-64'])
        except:
            age60_64=0
        try:
            age65_69 = float(data['data']['age']['65-69'])
        except:
            age65_69=0
        try:
            age70_74 = float(data['data']['age']['70-74'])
        except:
            age70_74=0
        try:
            age75_79 = float(data['data']['age']['75-79'])
        except:
            age75_79=0
        try:
            age80_84 = float(data['data']['age']['80-84'])
        except:
            age80_84=0
        try:
            age85_89 = float(data['data']['age']['85-89'])
        except:
            age85_89=0

        try:
            proportion_with_degree = float(data['data']['proportion_with_degree'])
        except:
            proportion_with_degree=0
        try:
            vehicles_per_household = float(data['data']['vehicles_per_household'])
        except:
            vehicles_per_household=0
        try:
            commute_method_foot = float(data['data']['commute_method']['foot'])
        except:
            commute_method_foot=0
        try:
            commute_method_bicycle = float(data['data']['commute_method']['bicycle'])
        except:
            commute_method_bicycle=0
        try:
            commute_method_other = float(data['data']['commute_method']['other'])  
        except:
            commute_method_other=0
        try:
            commute_method_motorcycle = float(data['data']['commute_method']['motorcycle'])  
        except:
            commute_method_motorcycle=0
        try:
            commute_method_taxi = float(data['data']['commute_method']['taxi'])  
        except:
            commute_method_taxi=0
        try:
            commute_method_train = float(data['data']['commute_method']['train']) 
        except:
            commute_method_train=0 
        try:
            commute_method_bus = float(data['data']['commute_method']['bus'])
        except:
            commute_method_bus=0
        try:
            commute_method_underground_light_rail = float(data['data']['commute_method']['underground_light_rail']) 
        except:
            commute_method_underground_light_rail=0
        try:
            commute_method_car_driver = float(data['data']['commute_method']['car_driver'])   
        except:
            commute_method_car_driver=0
        try:
            commute_method_at_home = float(data['data']['commute_method']['at_home']) 
        except:
            commute_method_at_home=0
        try:
            commute_method_car_passenger = float(data['data']['commute_method']['car_passenger']) 
        except:
            commute_method_car_passenger=0
        try:
            social_grade_ab = float(data['data']['social_grade']['ab']) 
        except:
            social_grade_ab=0
        try:
            social_grade_de = float(data['data']['social_grade']['de'])
        except:
            social_grade_de=0
        try:
            social_grade_c1 = float(data['data']['social_grade']['c1'])
        except:
            social_grade_c1=0
        try:
            social_grade_c2 = float(data['data']['social_grade']['c2'])
        except:
            social_grade_c2=0
    else:
        print(data)
        pass

    record = [ code,
    Year_1_Value, Year_2_Value, Year_2_growth, Year_3_Value, Year_3_growth, Year_4_Value, Year_4_growth, Year_5_Value,Year_5_growth,
    population, crimes_last_12m, crimes_per_thousand, crime_rating, PublicOrder,
    Burglary, Robbery, PossessionOfWeapons, BicycleTheft, AntiSocialBehaviour, Violence,
    Theft, Shoplifting, OtherCrime, Drugs, OtherTheft, VehicleCrime, CriminalDamage,
    deprivation, health, age0_4, age5_9, age10_14, age15_19, age20_24, age25_29, age30_34, age35_39,
    age40_44, age45_49, age50_54, age55_59, age60_64, age65_69, age70_74, age75_79, age80_84, age85_89,
    proportion_with_degree, vehicles_per_household, commute_method_foot,commute_method_bicycle,
    commute_method_other, commute_method_motorcycle,commute_method_taxi,commute_method_train,
    commute_method_bus, commute_method_underground_light_rail,commute_method_car_driver, 
    commute_method_at_home, commute_method_car_passenger,social_grade_ab, social_grade_de,
    social_grade_c1, social_grade_c2]

    csvDatawriter.writerow(record)



fileDataCSV.close()  
