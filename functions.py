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


"""
This function download facilities from OSM database and considering it as a polygon features.
"""
def ETL_facility_polygon (group,values):
    """Download facilities from OSM

    Args:
        group (str): the name of type tags
        values (str): the classification inside every group

    Returns:
        geodataframe: type(fac_polygon)
    """
    
    #download facilities from OSM
    fac_polygon= osm.geometries_from_place("Lisbon",tags={group:values})

    #As building group does not have "amenity" column, but the information is on "building" columns, we rename it as "amenity"
    if group=='building':
        fac_polygon.drop(['amenity'],axis=1,inplace=True)
        fac_polygon = fac_polygon.rename(columns={"building":"amenity"})
        
    #to filter the columns that we want
    fac_polygon=fac_polygon[['geometry','amenity','name','addr:postcode','addr:street','email','website','addr:housenumber','phone','contact:email','contact:website','contact:phone']].reset_index()
    fac_polygon['email'] = fac_polygon['email'].fillna(fac_polygon.pop('contact:email'))
    fac_polygon['phone'] = fac_polygon['phone'].fillna(fac_polygon.pop('contact:phone'))
    fac_polygon['website'] = fac_polygon['website'].fillna(fac_polygon.pop('contact:website'))

    
    #to concatenate the address
    fac_polygon['address']=fac_polygon['addr:street']+', Nº '+fac_polygon['addr:housenumber']+' - Postal Code: '+fac_polygon['addr:postcode']
    fac_polygon= fac_polygon.drop(columns=['addr:street','addr:housenumber','addr:postcode'])
    
    # Rename columns to match the database model
    fac_polygon = fac_polygon.rename(columns={
        "addr:street":"address",
        "addr:postcode":"postal_cod",
        "amenity":"facility",
        "phone":"phone_number"})
        
    #to filter only the geometry that we want
    fac_polygon=fac_polygon.query("element_type != 'node'")

    #to change multipolygon to polygon
    fac_polygon=fac_polygon.explode('geometry')

   
    return fac_polygon

"""
This function download facilities from OSM database and considering it as a point features.
"""
def ETL_facility_point (group,values):
    """Download facilities from OSM

    Args:
        group (str): the name of type tags
        values (str): the classification inside every group

    Returns:
        geodataframe: type(fac_amenities_point_final)
    """
    fac_point = osm.geometries_from_place("Lisbon",tags={group:values})

    if group=='building':
            fac_point.drop(['amenity'],axis=1,inplace=True)
            fac_point = fac_point.rename(columns={"building":"amenity"})
     
    try:
        fac_point=fac_point[['geometry','amenity','name','addr:postcode','addr:street','email','website','addr:housenumber','phone','contact:phone','contact:website','contact:email','opening_hours','brand']].reset_index()
        fac_point['email'] = fac_point['email'].fillna(fac_point.pop('contact:email')) 
        fac_point['phone'] = fac_point['phone'].fillna(fac_point.pop('contact:phone'))
        fac_point['website'] = fac_point['website'].fillna(fac_point.pop('contact:website'))
        fac_point['name'] = fac_point['name'].fillna(fac_point.pop('brand'))
    except:
        fac_point=fac_point[['geometry','amenity','name','addr:postcode','addr:street','email','website','addr:housenumber','phone','contact:phone','contact:website','opening_hours']].reset_index()
        fac_point['phone'] = fac_point['phone'].fillna(fac_point.pop('contact:phone'))
        fac_point['website'] = fac_point['website'].fillna(fac_point.pop('contact:website'))
        

    #to concatenate the address
    fac_point['address']=fac_point['addr:street']+', Nº '+fac_point['addr:housenumber']+' - Postal Code: '+fac_point['addr:postcode']
    fac_point= fac_point.drop(columns=['addr:street','addr:housenumber','addr:postcode'])


    # Rename columns to match the database model
    fac_point = fac_point.rename(columns={
        "addr:street":"address",
        "addr:postcode":"postal_cod",
        "amenity":"facility",
        "phone":"phone_number"})


    #to filter only the geometry that we want
    fac_point_point=fac_point.query("element_type == 'node'")
    fac_point_polygon=fac_point.query("element_type != 'node'")
    
    #change the geo crs to project crs
    fac_amenities_point_polygon2=fac_point_polygon.to_crs({"init":"epsg:32629"})

    #creating centroids
    fac_amenities_point_polygon2['geometry'] = fac_amenities_point_polygon2.centroid

    #change the project crs to geo crs
    fac_amenities_point_polygon3=fac_amenities_point_polygon2.to_crs({"init":"epsg:4326"})

    #changing the points to wgs84 again to avoid some problems on the crs
    fac_amenities_point_point2=fac_point_point.to_crs({"init":"EPSG:4326"})

    fac_amenities_point_final = pd.concat([fac_amenities_point_point2 ,fac_amenities_point_polygon3], ignore_index=True , sort= False)
    
    return fac_amenities_point_final




