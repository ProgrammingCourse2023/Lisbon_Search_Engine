![Captura de pantalla 2023-02-22 153415](https://user-images.githubusercontent.com/126191930/221417611-623cca0e-6765-4466-b9d4-10a4a3508ee8.jpg)


# Lisbon Search Engine

This repository presents the final project of programming seminar 2023 in master of Geospatial technologies.
As part of the advance of geolocalization, the identification and display position of representative places in the development of communities have meaningful importance currently, this project seeks to display facilities in the city of Lisbon through the use of the "Lisbon Search Engine".
The development of this tool was possible due to the creation of the ETL to do the extraction, transformation and load of public data into the database of the project, so connecting it to the API according to the request done by the users using the front end of the tool.

The objective of the tool is allow to the user select specific facilities located in the city of Lisbon and display their main information such as name, address, email, phone, website, among others.----

If it is necessary, you can create a lisbon_engine environment in Anaconda to run this application, running the code below:

    conda create -n lisbon_engine

    conda activate lisbon_engine

After it, you need to install all the packages necessary for this application running the code below:

    conda install --file requirements.txt --channel conda-forge
  

Considering database used in this project, in the folder "database" are located 2 files to run it into PGAdmin considering all the configurations necessary.


# Data

To reach the main objective of Lisbon Search Engine the data was extract from Open Street Map (OSM), the tool aim displaying the most usual facilities due to the users are continuously searching this information. This choice is taken as part of first version of the tool; however, for future versions will be included other primary features OSM classification.

The facilities chosen were divided into two categories, depending of which geometry were thought to display on the map. For example, facilities who have a big dimension on field (Hospitals, Universities, Schools) will be displayed on the map using polygon geometries from OSM. In other hand, facilities which dimension are not too big were displayed as point geometries. The geometric transformations were done in the [ETL script](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/blob/main/ETL/functions.py).

# Database
The database project "programming_ project" was created through the use of PGadmin and we used the extension PostGIS to work with the geometries inside the tables. The tables and views used on ETL and API scripts were created using SQL scripts that are inside the [database folder](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/tree/main/DB) to run it in sequencial order. The database has one table and one view per geometry. For example, "facilities_point" as the table and "facilities_point_geojson" as the view

# ETL
The extraction of the information from Open Street Map was possible using the "geometries_from_place()" inside the OSM package, where "group" are the OSM main classification (amenity, building) and "values" are the facilities (hospital, library, school, etc). Also, it was setting the "location" query, which represents the name of a city, region or country. As aim of the project was defined "Lisbon" as the location query, but other places can be chosen as well. The code below shows how the OSM tool works
     
     osm.geometries_from_place("place",tags={group:values})
     
     example = osm.geometries_from_place("Lisbon",tags={amenity:hospital})


After download the data, the script does some transformations on the table, for example maintaining the most important columns from OSM table to the users, renaming some columns, concatening other to have the information into a single column.

About the geometry, the function applied on polygon classes (explain in the "Data" chapter) were filtered only to maintain polygon geometry, while the point classes were divided between point and polygon to transform the polygon into points and insert it again to the points from OSM. It was decided because it could be difficult to create a polygon from a simple point to represent well the facilities on the terrain, but it is possible to transform a polygon into a point and maintain the original information from the table. ----

The extraction and transformation steps were put inside two functions developed in our script: "ETL_facility_polygon" and "ETL_facility_point"

The data upload to the created database is not inside the function developed to allow the user a customization, if is necessary to change the final database. The loading function was done using to_postgis tool, from Geopandas package, that allow to insert data using a SQL connection in a table and with the geometry. The code below shows how the tool work.

        Geodataframe.to_postgis("table name",connection,if_exists='append', index=False, dtype={'column with geometry': Geometry(geometry_type='geometry choose', srid= SRID number)})
        where:
        append could be append/replace/fail
        
        example_polygon.to_postgis("facilities_polygon",LINK_DB,if_exists='append', index=False, dtype={'geometry': Geometry(geometry_type='POLYGON', srid= 4326)})




# API

In the API part some functions were develop to the user get:
- all information from the database considering a geometry ("/facilities_point" and "/facilities_polygon");
- a specific information in each table using an ID number ("/facilities_point/<id>" and "/facilities_polygon/<id>");
- a search connected with the front-end to show the results in a map 






