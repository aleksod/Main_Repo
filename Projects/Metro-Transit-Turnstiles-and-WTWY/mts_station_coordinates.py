import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

df = pd.read_csv('http://web.mta.info/developers/data/nyct/subway/Stations.csv')

subset = df[['Stop Name', 'GTFS Latitude', 'GTFS Longitude']]
coord_data = subset[(subset['GTFS Latitude'] >= 40.731191) &
                     (subset['GTFS Latitude'] <= 40.753512) &
                     (subset['GTFS Longitude'] >= -74.001387) &
                     (subset['GTFS Longitude'] <= -73.977641)]
# subset3 = coord_data.drop_duplicates('Stop Name')

'''
The next lines clean up the coordinates data frame and aling station names with
those in the main data frame.
'''
coord_data.rename(columns={'Stop Name': 'STATION'}, inplace=True)
coord_data['STATION'] = coord_data['STATION'].str.upper()
coord_data['STATION'] = coord_data['STATION'].str.replace(' - ','-')
coord_data['STATION'] = coord_data['STATION'].str.upper()
coord_data['STATION'] = coord_data['STATION'].str.replace('STATION', 'STA')
coord_data['STATION'] = coord_data['STATION'].str.replace('GRAND CENTRAL-42 ST', 'GRD CNTRL-42 ST')
coord_data = coord_data.rename(columns={'GTFS Latitude': 'Lat', 'GTFS Longitude': 'Long'})

with open('coord_data.pkl', 'wb') as f:
    pickle.dump(coord_data, f)
