import googlemaps
from datetime import datetime
import pickle
import pandas as pd
import csv

# Load POIs data using Google places API
#
# uses postcodes from LondonPostcodes.csv
#
# POIs data is saved on a csv files ListOfIDs_<POIs_type>.csv
#
# status: on drive

gmaps = googlemaps.Client(key='AIzaSyDxxxxxxxxxxxxxxxxxx')

District = "Lambeth"
ResetStoredData = True # If False append new data to DB or pickle
UpdateDB = False # If False save to pickle
Aggregation_level = 5 # 5 - codepost 4- section 2- area 1- district
PriodicSave = 100 # Save after N Calls
fields = ['place_id', 'name', 'formatted_address', 'lat','lng','types','rating','price_level']

#Used for testing 
test_PostCode = "E1 4D"
test_POI_type = "subway_station"
test_Aggregation_level = 5

# List of POI_types, Aggregation_level 6 - codepost 5, 4- section 2- area 
POIS = [
    ["subway_station", 6 ],
    ["train_station", 6 ],
    ["university", 6 ],
    ["secondary_school", 6 ],
    ["primary_school", 6 ],
    ["school", 6 ],
    ["parking", 6 ],
    ["park", 6 ],
    ["shopping_mall", 6 ],
    ["hospital", 6 ],
    ["mosque", 6 ],
    ["police", 6 ],
    ["synagogue", 6 ],
    ["cemetery", 6 ],
    ["church", 6 ],
    ["fire_station", 6 ],
    ["hindu_temple", 6 ],
    ["restaurant", 6 ],
    ["bar", 6 ],
    ["cafe", 6 ],
    ["supermarket", 6 ],
    ]
 

def select(code,PostCode,Aggregation_level):
    return PostCode[:Aggregation_level] in code


# Load ALL code posts
df = pd.read_csv('../LondonPostcodes.csv', delimiter=',')


# Select District data
df_aux = df[df['District'] == District]

# Select Posts codes: with test restriction 
postcodes = set(df_aux['Postcode'])
print("Number of Postcodes: ", len(postcodes))

for place_type,Aggregation_level in POIS:
    print("----------------")
    print("------", place_type)

    slectedAgg = { x[:Aggregation_level] for x in postcodes }

    print(slectedAgg)
    print("Number of Codes: ", len(slectedAgg))

    # Get data
    count = 1
    dataS = []

    if not UpdateDB:
        if ResetStoredData:
            fileCSV = open('ListOfIDs_'+ place_type +'.csv', 'w')
            csvwriter = csv.writer(fileCSV)
            # writing the fields  
            csvwriter.writerow(fields)
            ExistPOIs = []

        else:
            # Read existen places:
            dfPOI = pd.read_csv('ListOfIDs_'+ place_type +'.csv', delimiter=',')
            ExistPOIs = list(dfPOI['place_id'])

            fileCSV = open('ListOfIDs_'+ place_type +'.csv', 'a')
            csvwriter = csv.writer(fileCSV)

    for postcode in slectedAgg:

        data = gmaps.places( query=postcode+", London, UK",  type=place_type, language="en")
        
        if data['status'] == "OK":
            print('code:',postcode,'OK')
            for item in data['results']:

                try:
                    place_id = item['place_id']
                except:
                    place_id = ''
                
                try:
                    name = item['name']
                except:
                    name = '' 

                try:
                    address  = item['formatted_address']
                    #if not codepost in address:
                    #    break
                except:
                    address = '' 

                try:
                    lat = item['geometry']['location']['lat']
                except:
                    lat = 0

                try:
                    lng = item['geometry']['location']['lng']
                except:
                    lng = 0

                try:
                    item_type = item['types']
                    if not place_type in item_type:
                        break
                    item_type = place_type
                except:
                    item_type = ''

                try:
                    rating = item['rating']
                except:
                    rating = 0

                try:
                    user_ratings_total = item['user_ratings_total']
                except:
                    user_ratings_total = 0

                try:
                    price_level = item['price_level']
                except:
                    price_level =  0

                record = [place_id,name,address,lat,lng,item_type,rating,price_level]

                if place_id not in ExistPOIs: # Only store not existent places
                    dataS.append(record)
                    ExistPOIs.append(place_id)

                count += 1
        else:
            print('code:',postcode,'Error')

        if count>PriodicSave:
            if not UpdateDB:
                #for record in dataS:
                #    print(record)
                #    # writing the data rows  
                csvwriter.writerows(dataS)
                dataS = []
                count = 0
        


    if not UpdateDB and dataS:
        csvwriter.writerows(dataS)

    fileCSV.close()


