from datetime import datetime
import pickle
import pandas as pd
import csv
import time

#
# Used to merge all data files:
#
#   postcodesynagogueData.csv
#   postcodeshopping_mallData.csv
#   postcodesecondaryData.csv
#   postcodeschoolData.csv
#   postcodeprimaryData.csv
#   postcodepoliceData.csv
#   postcodeprimaryData.csv
#   ...
#   EPCstatistics.csv
#   LondonPostcodes.csv
#
# Output: googlePlaces.csv info of all codeposts
#
# Merge googlePlaces.csv with
#
#   areaCodeData.csv
#   postCodeData.csv
#
# Output: datasetV7.csv

def Date(date_string):
   fmt = '%Y-%m-%d' # Choose fmt according to your format
   return datetime.strptime(date_string,fmt)

Dataset = pd.read_csv('../PlacesSearch/postcodesynagogueData.csv')
Dataset1 = pd.read_csv('../PlacesSearch/postcodeshopping_mallData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodesecondaryData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeschoolData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeprimaryData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodepoliceData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeparkingData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeparkData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodemosqueData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodefire_stationData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodehindu_templeData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodecemeteryData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeuniversityData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodetrain_stationData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodehospitalData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodecafeData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodesupermarketData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodesubway_stationData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeBarsData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset1 = pd.read_csv('../PlacesSearch/postcodeResturantsData.csv')
Dataset = pd.merge(Dataset, Dataset1, on="code")

Dataset.rename(columns={'code':'postcode'}, inplace=True)

Dataset1 = pd.read_csv('../MergePPCert/EPCstatistics.csv')

Dataset = pd.merge(Dataset, Dataset1, on="postcode")

LondonPostcodes = pd.read_csv('../PostCodeLookup/LondonPostcodes.csv')


Dataset1 = pd.DataFrame()
Dataset1['postcode'] = LondonPostcodes['Postcode']
Dataset1['postcode_Latitude'] = LondonPostcodes['Latitude']
Dataset1['postcode_Longitude'] = LondonPostcodes['Longitude']
Dataset1['MSOA_Code'] = LondonPostcodes['MSOA Code']
Dataset1['LSOA_Code'] = LondonPostcodes['LSOA Code']
Dataset1['Distance_to_station'] = LondonPostcodes['Distance to station']
Dataset1['Average_Income'] = LondonPostcodes['Average Income']
Dataset1['Population'] = LondonPostcodes['Population']
Dataset1['Households'] = LondonPostcodes['Households']

Dataset1.drop_duplicates(subset=['postcode'], keep='last',inplace=True)

Dataset = pd.merge(Dataset, Dataset1, on="postcode")

del(LondonPostcodes)

Dataset.to_csv("googlePlaces.csv")

print(len(Dataset))

Dataset1 = pd.read_csv('../PropertyData/areaCodeData.csv')
Dataset1.rename(columns={'code':'postcode'}, inplace=True)

Dataset = pd.merge(Dataset, Dataset1, on="postcode")
print(len(Dataset))

Dataset1 = pd.read_csv('../PropertyData/postCodeData.csv')
Dataset1.rename(columns={'code':'postcode'}, inplace=True)

Dataset = pd.merge(Dataset, Dataset1, on="postcode")
print(len(Dataset))

#Dataset1 = pd.read_csv('../PropertyData/postCodePlaceData.csv')
#Dataset1.rename(columns={'code':'postcode'}, inplace=True)

#Dataset = pd.merge(Dataset, Dataset1, on="postcode")
#print(len(Dataset))

#Dataset1 = pd.read_csv('../PropertyData/postCodeSchoolsData.csv')
#Dataset1.rename(columns={'code':'postcode'}, inplace=True)

#Dataset = pd.merge(Dataset, Dataset1, on="postcode")
#print(len(Dataset))

Dataset.to_csv("datasetV7.csv")

