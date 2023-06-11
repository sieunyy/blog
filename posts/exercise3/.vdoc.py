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
#
#
#
#
#
#
#
#
import pandas as pd
import geopandas as gpd

import folium
from folium import Choropleth
from folium.plugins import HeatMap
#
#
#
#
#
#
#
def embed_map(m, file_name):
    from IPython.display import IFrame
    m.save(file_name)
    return IFrame(file_name, width='100%', height='500px')
#
#
#
#
#
#
#
#
#
plate_boundaries = gpd.read_file("../data/Plate_Boundaries/Plate_Boundaries/Plate_Boundaries.shp")
plate_boundaries['coordinates'] = plate_boundaries.apply(lambda x: [(b,a) for (a,b) in list(x.geometry.coords)], axis='columns')
plate_boundaries.drop('geometry', axis=1, inplace=True)

plate_boundaries.head()
#
#
#
#
#
# Load the data and print the first 5 rows
earthquakes = pd.read_csv("../../../spatial_analysis/data/earthquakes1970-2014.csv", parse_dates=["DateTime"])
earthquakes.head()
#
#
#
#
#
# Create a base map with plate boundaries
m_1 = folium.Map(location=[35,136], tiles='cartodbpositron', zoom_start=5)
for i in range(len(plate_boundaries)):
    folium.PolyLine(locations=plate_boundaries.coordinates.iloc[i], weight=2, color='black').add_to(m_1)

# Add a heatmap to the map
HeatMap(data = earthquakes[['Latitude', 'Longitude']], radius = 15).add_to(m_1)

# Show the map
embed_map(m_1, 'q_1.html')

m_1
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
# Create a base map with plate boundaries
m_2 = folium.Map(location=[35, 136], tiles = 'cartodbpositron', zoom_start = 5)

def color_producer(val):
    if val < 50:
        return 'forestgreen'
    elif val < 100:
        return 'darkorange'
    else:
        return 'darkred'

for i in range(len(plate_boundaries)):
    folium.PolyLine(locations = plate_boundaries.coordinates.iloc[i], weight = 2, color = 'black').add_to(m_2)
    
# Add a map to visualize earthquake depth
for i in range(0, len(earthquakes)):
    folium.Circle(
        location = [earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        radius=2000,
        color = color_producer(earthquakes.iloc[i]['Depth'])).add_to(m_2)

# View the map
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
# GeoDataFrame with prefecture boundaries
prefectures = gpd.read_file("../../../spatial_analysis/data/japan-prefecture-boundaries/japan-prefecture-boundaries/japan-prefecture-boundaries.shp")
prefectures.set_index('prefecture', inplace=True)
prefectures.head()
#
#
#
#
#
# DataFrame containing population of each prefecture
population = pd.read_csv("../../../spatial_analysis/data/japan-prefecture-population.csv")
population.set_index('prefecture', inplace = True)

# Calculate area (in square kilometers) of each prefecture
area_sqkm = pd.Series(prefectures.geometry.to_crs(epsg=32654).area / 10**6, name = 'area_sqkm')
stats = population.join(area_sqkm)

# Add density (per square kilometer) of each prefecture
stats['density'] = stats["population"] / stats["area_sqkm"]
stats.head()
#
#
#
#
#
# Create a base map
m_3 = folium.Map(location = [35, 136], tiles = 'cartodbpositron', zoom_start = 5)

# Create a choropleth map to visualize population density
Choropleth(geo_data = prefectures.__geo_interface__, 
           data = stats['density'], 
           key_on = "feature.id", 
           fill_color = 'YlGnBu', 
           legend_name = 'Population Density (per km²)'
          ).add_to(m_3)

# View the map
embed_map(m_3, 'q_3.html')

m_3
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
# Create a base map
m_4 = folium.Map(location = [35, 136], tiles = 'cartodbpositron', zoom_start = 5)

def color_producer(magnitude):
    if magnitude > 6.5:
        return 'red'
    else:
        return 'green'

# Create a map
Choropleth(geo_data = prefectures.__geo_interface__, 
           data = stats['density'], 
           key_on = "feature.id", 
           fill_color = 'YlGnBu', 
           legend_name = 'Population Density (per km²)'
          ).add_to(m_4)

for i in range(0, len(earthquakes)):
    folium.Circle(
        location = [earthquakes.iloc[i]['Latitude'], earthquakes.iloc[i]['Longitude']],
        popup = ("{} ({})").format(earthquakes.iloc[i]['Magnitude'], earthquakes.iloc[i]['DateTime'].year),
        radius = earthquakes.iloc[i]['Magnitude']**5.5,
        color = color_producer(earthquakes.iloc[i]['Magnitude'])).add_to(m_4)

# View the map
embed_map(m_4, 'q_4.html')

m_4
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
