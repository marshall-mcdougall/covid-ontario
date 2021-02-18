import urllib
import pandas as pd
pd.set_option('display.max_rows', 500)
import requests
import json
import numpy as np

#-------------------------------------
# Ontario Vaccine Data Pull
# Datasource URL: https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a89caa9-511c-4568-af89-7f2174b4378c
vaccine_url='https://data.ontario.ca/api/3/action/datastore_search?resource_id=8a89caa9-511c-4568-af89-7f2174b4378c'
vaccine_url_limit=vaccine_url+'&limit='
vaccine_data=requests.get(vaccine_url)
vaccine_json_object=json.loads(vaccine_data.content)
vaccine_limit=vaccine_json_object['result']['total']

vaccine_data_total=requests.get(vaccine_url_limit+str(vaccine_limit))
vaccine_json_object_total=json.loads(vaccine_data_total.content)

vaccine_data_points=[]
for row in vaccine_json_object_total['result']['records']:
    vaccine_data_points.append(row)

pd.DataFrame(vaccine_data_points).to_csv('ontario-vaccine-progress.csv')

#-------------------------------------
# Ontario Case Data Pull
# Datasource URL: https://data.ontario.ca/dataset/status-of-covid-19-cases-in-ontario-by-public-health-unit-phu/resource/d1bfe1ad-6575-4352-8302-09ca81f7ddfc
case_url='https://data.ontario.ca/api/3/action/datastore_search?resource_id=d1bfe1ad-6575-4352-8302-09ca81f7ddfc'
case_url_limit=case_url+'&limit='
case_data=requests.get(case_url)
case_json_object=json.loads(case_data.content)
case_limit=case_json_object['result']['total']

case_data_total=requests.get(case_url_limit+str(case_limit))
case_json_object_total=json.loads(case_data_total.content)

case_data_points=[]
for row in case_json_object_total['result']['records']:
    case_data_points.append(row)

pd.DataFrame(case_data_points).to_csv('ontario-case-data.csv')

#-------------------------------------
# Ontario Color Zone Data Pull
# Datasource URL: https://data.ontario.ca/dataset/ontario-covid-19-zones/resource/ce9f043d-f0d4-40f0-9b96-4c8a83ded3f6
zone_url='https://data.ontario.ca/api/3/action/datastore_search?resource_id=ce9f043d-f0d4-40f0-9b96-4c8a83ded3f6'
zone_url_limit=zone_url+'&limit='
zone_data=requests.get(zone_url)
zone_json_object=json.loads(zone_data.content)
zone_limit=zone_json_object['result']['total']

zone_data_total=requests.get(zone_url_limit+str(zone_limit))
zone_json_object_total=json.loads(zone_data_total.content)

zone_data_points=[]
for row in zone_json_object_total['result']['records']:
    zone_data_points.append(row)

color_status = pd.DataFrame(zone_data_points)
reporting_phu = color_status['Reporting_PHU'].drop_duplicates().tolist()

color_status['Active'] = 'Not Active'

for phu in reporting_phu:
    temp = color_status[color_status['Reporting_PHU'] == phu]
    max_id = temp['_id'].max()
    max_id = max_id - 1
    color_status.loc[max_id, 'Active'] = 'Active'

color_status.to_csv('ontario-covid-color-status.csv')