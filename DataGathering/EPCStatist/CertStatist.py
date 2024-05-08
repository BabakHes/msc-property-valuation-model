from datetime import datetime
import pickle
import pandas as pd
import csv
import time

District = "Lambeth"

fields = ['postcode', 'area', 'count', 'area_min', 'area_max', 'area_mean',  'area_std', 'construction_before_1900', 'construction_1900_1929', 'construction_1930_1949', 
   'construction_1950_1966', 'construction_1967_1975', 'construction_1976_1982', 'construction_1983_1990', 'construction_1991_1995',
   'construction_1996_2002', 'construction_2003_2006', 'construction_2007_2011', 'construction_2012_onwards']

def select(date_string,y):
   fmt = '%Y-%m-%d' # Choose fmt according to your format

   return datetime.strptime(date_string,fmt).year

# Load ALL code posts
df = pd.read_csv('../LondonPostcodes.csv', delimiter=',')


# Select District data
df_aux = df[df['District'] == District]

# Select Posts codes: with test restriction 
postcodes = set(df_aux['Postcode'])

cert= pd.read_csv('./certificates.csv')

fileCSV = open('EPCstatistics.csv', 'w')
csvwriter = csv.writer(fileCSV)
csvwriter.writerow(fields)

for code in postcodes:
   print('-- L1')
   data = cert[cert['POSTCODE'] == code].copy()
   count = 0
   if len(data)==0:
      w = code.split()
      p1 = w[0]
      p2 = w[1][0]
      print('-- L2')
      data = cert[cert['POSTCODE'].apply(lambda x: p1+' '+p2 in x)].copy()
      if len(data)==0:
         data = cert[cert['POSTCODE'].apply(lambda x: p1 in x)].copy()
         print('-- L3')

   describe = data['TOTAL_FLOOR_AREA'].describe()

   count = describe.loc['count']
   area_min = describe.loc['min']
   area_max = describe.loc['max']
   area_mean = describe.loc['mean']
   area_std = describe.loc['std']

   construction_before_1900 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: before 1900'])/count
   construction_1900_1929 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1900-1929'])/count
   construction_1930_1949 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1930-1949'])/count
   construction_1950_1966 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1950-1966'])/count
   construction_1967_1975 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1967-1975'])/count
   construction_1976_1982 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1976-1982'])/count
   construction_1983_1990 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1983-1990'])/count
   construction_1991_1995 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1991-1995'])/count
   construction_1996_2002 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 1996-2002'])/count
   construction_2003_2006 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 2003-2006'])/count
   construction_2007_2011 = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 2007-2011'])/count
   construction_2012_onwards = len(data[data['CONSTRUCTION_AGE_BAND']=='England and Wales: 2012 onwards'])/count

   record = [ code, code.split()[0], count, area_min, area_max, area_mean,  area_std, construction_before_1900, construction_1900_1929, construction_1930_1949, 
   construction_1950_1966, construction_1967_1975, construction_1976_1982, construction_1983_1990, construction_1991_1995,
   construction_1996_2002, construction_2003_2006, construction_2007_2011, construction_2012_onwards]

   csvwriter.writerow(record)

   print(code,count)

fileCSV.close()





