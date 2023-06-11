# type: ignore
# flake8: noqa
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
import math
import numpy as np
import pandas as pd
import geopandas as gpd
from geopy.geocoders import Nominatim            # What you'd normally run

import folium 
from folium import Marker
from folium.plugins import MarkerCluster
#
#
#
#
#
def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width = '100%', height = '500px')
#
#
#
#
#
#
#
#
#
# Load and preview Starbucks locations in California
starbucks = pd.read_csv("../../../spatial_analysis/data/starbucks_locations.csv")
starbucks.head()
#
#
#
#
#
# How many rows in each column have missing values?
print(starbucks.isnull().sum())

# View rows with missing locations
rows_with_missing = starbucks[starbucks["City"] == "Berkeley"]
rows_with_missing
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# Create the geocoder
geolocator = Nominatim(user_agent = "kaggle_learn")

def my_geocoder(row):
    try:
        point = geolocator.geocode(row).point
        return pd.Series({'Latitude': point.latitude, 'Longitude': point.longitude})
    except:
        return None

rows_with_missing[['Latitude', 'Longitude']] = rows_with_missing.apply(lambda x: my_geocoder(x['Address']), axis = 1)

starbucks.update(rows_with_missing[['Latitude', 'Longitude']])

print("{}% of addresses were geocoded!".format(
    (1 - sum(np.isnan(starbucks["Latitude"])) / len(starbucks)) * 100))
#
#
#
starbucks.head()
#
#
#
#
#
#
#
# Create a base map
m_2 = folium.Map(location = [37.88, -122.26], zoom_start = 13)

# Add a marker for each Berkeley location
for idx, row in starbucks[starbucks['City'] == 'Berkeley'].iterrows():
    Marker([row['Latitude'], row['Longitude']], popup = row['Store Name']).add_to(m_2)

# Show the map
embed_map(m_2, 'q_2.html')

m_2
#
#
#
#
#
#
#
#
#
CA_counties = gpd.read_file("../../../spatial_analysis/data/CA_county_boundaries/CA_county_boundaries/CA_county_boundaries.shp")
CA_counties.crs = {'init': 'epsg:4326'}
CA_counties.head()
#
#
#
#
#
#
#
#
CA_pop = pd.read_csv("../../../spatial_analysis/data/CA_county_population.csv", index_col="GEOID")
CA_high_earners = pd.read_csv("../../../spatial_analysis/data/CA_county_high_earners.csv", index_col="GEOID")
CA_median_age = pd.read_csv("../../../spatial_analysis/data/CA_county_median_age.csv", index_col="GEOID")
#
#
#
#
#
#
#
CA_join = CA_pop.join([CA_high_earners, CA_median_age]).reset_index()
CA_stats = CA_counties.merge(CA_join, on = "GEOID")
CA_stats.head()
#
#
#
#
#
CA_stats["density"] = CA_stats["population"] / CA_stats["area_sqkm"]
CA_stats.head()
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
sel_counties = CA_stats[(CA_stats['high_earners'] >= 100000) & (CA_stats['median_age'] < 38.5) & (CA_stats['density'] >= 285) &
                        ((CA_stats['high_earners'] >= 500000) | (CA_stats['median_age'] < 35.5) | (CA_stats['density'] >= 1400))]
sel_counties
#
#
#
#
#
#
#
#
#
starbucks_gdf = gpd.GeoDataFrame(starbucks, geometry = gpd.points_from_xy(starbucks.Longitude, starbucks.Latitude))
starbucks_gdf.crs = {'init': 'epsg:4326'}
starbucks_gdf.head()
#
#
#
#
#
county_stores = gpd.sjoin(sel_counties, starbucks_gdf)
num_stores = len(county_stores)
num_stores
#
#
#
#
#
#
#
# Create a base map
m_6 = folium.Map(location = [37, -120], zoom_start = 6)

# Show selected store locations
mc = MarkerCluster()

county_stores = gpd.sjoin(sel_counties, starbucks_gdf)

for idx, row in county_stores.iterrows() :
    if not math.isnan(row['Longitude']) and not math.isnan(row['Latitude']):
        mc.add_child(folium.Marker([row['Latitude'], row['Longitude']]))

m_6.add_child(mc)

# Show the map
embed_map(m_6, 'q_6.html')

m_6
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
