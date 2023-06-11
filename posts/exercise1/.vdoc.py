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
#
#
#
#
import geopandas as gpd
#
#
#
#
#
#
#
loans_filepath = "../../../spatial_analysis/data/kiva_loans/kiva_loans/kiva_loans.shp"

# Load the data
world_loans = gpd.read_file(loans_filepath)

# Uncomment to view the first five rows of the data
world_loans.head()
#
#
#
#
#
#
#
# This dataset is provided in GeoPandas
world_filepath = gpd.datasets.get_path('naturalearth_lowres')
world = gpd.read_file(world_filepath)
world.head()
#
#
#
#
#
ax = world.plot(figsize = (10, 10), color = 'whitesmoke', linestyle = ':', edgecolor = 'black')
world_loans.plot(markersize = 2, ax = ax)
#
#
#
#
#
#
#
PHL_loans = world_loans.loc[world_loans['country'] == 'Philippines'].copy()
PHL_loans.head()
#
#
#
#
#
#
#
# Load a KML file containing island boundaries
gpd.io.file.fiona.drvsupport.supported_drivers['KML'] = 'rw'
PHL = gpd.read_file("../../../spatial_analysis/data/Philippines_AL258.kml", driver='KML')
PHL.head()
#
#
#
#
#
ax = PHL.plot(figsize = (10, 10), color = 'whitesmoke', linestyle = ':', edgecolor = 'black')
PHL_loans.plot(markersize = 2, ax = ax)
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
