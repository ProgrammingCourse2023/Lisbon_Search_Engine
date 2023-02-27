import geopandas as gpd
import pandas as pd, json
import os
import json
import requests
import osmnx as osm
import psycopg2
import sqlalchemy as sql
import numpy 
import shapely
from geoalchemy2 import Geometry
import ETL.functions as functions

"""
Constants used to run this code

>>Pay attention on PORT<<

If you need to add more class of amenity or building, you can edit the list using Open Street Map classification.

"""
USERNAME = 'postgres'
PASSWORD = 'postgres'
HOST = 'localhost'
PORT = 5432
DB = 'programming_project'
AMENITY_LIST_POINT = ['library','clinic','pharmacy','nightclub','bank','theatre','police','post_office']
AMENITY_LIST_POLYGON = ["hospital",'school','university']
BUILDING_LIST_POINT = ["industrial",'church','mosque','college','fire_station']    
LINK_DB = sql.create_engine(f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB}")


#calling the function to download and upload the polygon from amenity to our database
amenity_polygon = functions.ETL_facility_polygon("amenity",AMENITY_LIST_POLYGON)
amenity_polygon.to_postgis("facilities_polygon",LINK_DB,if_exists='append', index=False, dtype={'geometry': Geometry(geometry_type='POLYGON', srid= 4326)})

#calling the function to download and upload the point from amenity to our database
amenity_point = functions.ETL_facility_point("amenity",AMENITY_LIST_POINT)
amenity_point.to_postgis("facilities_point",LINK_DB,if_exists='append', index=False, dtype={'geometry': Geometry(geometry_type='POINT', srid= 4326)})

#calling the function to download and upload the point from building to our database
building_point = functions.ETL_facility_point("building",BUILDING_LIST_POINT)
building_point.to_postgis("facilities_point",LINK_DB,if_exists='append', index=False, dtype={'geometry': Geometry(geometry_type='POINT', srid= 4326)})


