import requests

from datetime import datetime
import pickle
import pandas as pd
import csv
import time

resetScanning = False
key = "RKDUXQSVR0"
URL = "https://api.propertydata.co.uk/"
exist_codes = set()

fields = ['code','dyn_total_for_rent', 'dyn_transactions_per_month', 'dyn_turnover_per_month', 'dyn_months_of_inventory', 'dyn_days_on_market',
    'dyn_sold_points_analysed', 'dyn_sold_average', 'dyn_sold_70pc_rangeMIN', 'dyn_sold_70pc_rangeMAX', 'dyn_sold_80pc_rangeMIN',
    'dyn_sold_80pc_rangeMAX', 'dyn_sold_90pc_rangeMIN', 'dyn_sold_90pc_rangeMAX', 'dyn_sold_100pc_rangeMIN', 'dyn_sold_100pc_rangeMAX',
    'dyn_sold_sqf_points_analysed', 'dyn_sold_sqf_average', 'dyn_sold_sqf_70pc_rangeMIN', 'dyn_sold_sqf_70pc_rangeMAX', 'dyn_sold_sqf_80pc_rangeMIN',
    'dyn_sold_sqf_80pc_rangeMAX', 'dyn_sold_sqf_90pc_rangeMIN', 'dyn_sold_sqf_90pc_rangeMAX', 'dyn_sold_sqf_100pc_rangeMIN', 'dyn_sold_sqf_100pc_rangeMAX',
    'dyn_rents_points_analysed', 'dyn_rents_average', 'dyn_rents_70pc_rangeMIN', 'dyn_rents_70pc_rangeMAX', 'dyn_rents_80pc_rangeMIN',
    'dyn_rents_80pc_rangeMAX', 'dyn_rents_90pc_rangeMIN', 'dyn_rents_90pc_rangeMAX', 'dyn_rents_100pc_rangeMIN', 'dyn_rents_100pc_rangeMAX',
    'dyn_ptal', 'dyn_flood_risk','dyn_mean_area']

if resetScanning:

    fileDataCSV = open('postCodeData.csv', 'w')
    csvDatawriter = csv.writer(fileDataCSV)
    csvDatawriter.writerow(fields)
else:

    exist = pd.read_csv('postCodeData.csv')
    exist_codes = set(exist['code'])
    del(exist)

    fileDataCSV = open('postCodeData.csv', 'a+', newline='')
    csvDatawriter = csv.writer(fileDataCSV)


properties = pd.read_csv('../MergePPCert/UseOnlyPP.csv')

codes = set(properties['postcode']) - exist_codes

print(codes)
print(len(codes))

for code in codes:

    print(code)


    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'key': key , "postcode": code, 'points':50}


    endpoint = "demand-rent"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    
    if data['status'] == "success":

        total_for_rent = data['total_for_rent']
        transactions_per_month = data['transactions_per_month']
        turnover_per_month = float(data['turnover_per_month'][:-1])
        months_of_inventory = data['months_of_inventory']
        days_on_market = data['days_on_market']
    else:
        total_for_rent = 0
        transactions_per_month = 0
        turnover_per_month = 0
        months_of_inventory = 0
        days_on_market = 0
    
    endpoint = "sold-prices"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()
    
    if data['status'] == "success":
        sold_points_analysed = data['data']['points_analysed']
        sold_average = data['data']['average']
        sold_70pc_rangeMIN = data['data']['70pc_range'][0]
        sold_70pc_rangeMAX = data['data']['70pc_range'][1]
        sold_80pc_rangeMIN = data['data']['80pc_range'][0]
        sold_80pc_rangeMAX = data['data']['80pc_range'][1]
        sold_90pc_rangeMIN = data['data']['90pc_range'][0]
        sold_90pc_rangeMAX = data['data']['90pc_range'][1]
        sold_100pc_rangeMIN = data['data']['100pc_range'][0]
        sold_100pc_rangeMAX = data['data']['100pc_range'][1]
    else:
        print("sold-prices",data)
        pass

    endpoint = "sold-prices-per-sqf"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    if data['status'] == "success":

        sold_sqf_points_analysed = data['data']['points_analysed']
        sold_sqf_average = data['data']['average']
        sold_sqf_70pc_rangeMIN = data['data']['70pc_range'][0]
        sold_sqf_70pc_rangeMAX = data['data']['70pc_range'][1]
        sold_sqf_80pc_rangeMIN = data['data']['80pc_range'][0]
        sold_sqf_80pc_rangeMAX = data['data']['80pc_range'][1]
        sold_sqf_90pc_rangeMIN = data['data']['90pc_range'][0]
        sold_sqf_90pc_rangeMAX = data['data']['90pc_range'][1]
        sold_sqf_100pc_rangeMIN = data['data']['100pc_range'][0]
        sold_sqf_100pc_rangeMAX = data['data']['100pc_range'][1]
    else:
        print("sold-prices-per-sqf",data)
        pass
    
    endpoint = "rents"
    
    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()


    if data['status'] == "success":
        rents_points_analysed = data['data']['long_let']['points_analysed']
        rents_average = data['data']['long_let']['average']
        rents_70pc_rangeMIN = data['data']['long_let']['70pc_range'][0]
        rents_70pc_rangeMAX = data['data']['long_let']['70pc_range'][1]
        rents_80pc_rangeMIN = data['data']['long_let']['80pc_range'][0]
        rents_80pc_rangeMAX = data['data']['long_let']['80pc_range'][1]
        rents_90pc_rangeMIN = data['data']['long_let']['90pc_range'][0]
        rents_90pc_rangeMAX = data['data']['long_let']['90pc_range'][1]
        rents_100pc_rangeMIN = data['data']['long_let']['100pc_range'][0]
        rents_100pc_rangeMAX = data['data']['long_let']['100pc_range'][1]
    else:
        print("rents",data)
        pass

    endpoint = "ptal"
    
    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    if data['status'] == "success":
        ptal = data['ptal']
    else:
        print("ptal",data)
        pass

    
    endpoint = "flood-risk"

    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    if data['status'] == "success":
        flood_risk = data['flood_risk']
    else:
        print("flood-risk",data)
        pass
    
    endpoint = "floor-areas"
    
    # sending get request and saving the response as response object
    time.sleep(3)
    r = requests.get(url = URL+endpoint, params = PARAMS)

    # extracting data in json format
    data = r.json()

    if data['status'] == "success":
        floor_areas = data['known_floor_areas']

        sum_areas = 0
        count_flat = 0
        for flat in floor_areas:
            sum_areas = flat['square_feet']
            count_flat += 1
        
        if count_flat:
            mean_area = sum_areas/count_flat
        else:
            mean_area = None
    else:
        print("floor-areas",data)
        pass

    record = [code,total_for_rent, transactions_per_month, turnover_per_month, months_of_inventory, days_on_market,
    sold_points_analysed, sold_average, sold_70pc_rangeMIN, sold_70pc_rangeMAX, sold_80pc_rangeMIN,
    sold_80pc_rangeMAX, sold_90pc_rangeMIN, sold_90pc_rangeMAX, sold_100pc_rangeMIN, sold_100pc_rangeMAX,
    sold_sqf_points_analysed, sold_sqf_average, sold_sqf_70pc_rangeMIN, sold_sqf_70pc_rangeMAX, sold_sqf_80pc_rangeMIN,
    sold_sqf_80pc_rangeMAX, sold_sqf_90pc_rangeMIN, sold_sqf_90pc_rangeMAX, sold_sqf_100pc_rangeMIN, sold_sqf_100pc_rangeMAX,
    rents_points_analysed, rents_average, rents_70pc_rangeMIN, rents_70pc_rangeMAX, rents_80pc_rangeMIN,
    rents_80pc_rangeMAX, rents_90pc_rangeMIN, rents_90pc_rangeMAX, rents_100pc_rangeMIN, rents_100pc_rangeMAX,
    ptal, flood_risk,mean_area]

    csvDatawriter.writerow(record)

fileCSV.close() 