# Lisbon Search Engine

This repository presents the final project of programming seminar 2023 in Erasmus Master Program in Geospatial Technologies.
As part of the advance of geolocalization, the identification and display position of representative places in the development of communities have meaningful importance currently, this project seeks to display facilities in the city of Lisbon through the use of the "Lisbon Search Engine".
The development of this tool was possible due to the creation of the ETL to do the extraction, transformation and load of public data into the database of the project, so connecting it to the API according to the request done by the users using the front end of the tool.

The objective of the tool is allow to the user select specific facilities located in the city of Lisbon and display their main information such as name, address, email, phone, website, among others.----


# Data

To reach the main objective of Lisbon Search Engine the data was extract from Open Street Map (OSM), the tool aim displaying the most usual facilities due to the users are continuously searching this information. This choice is taken as part of first version of the tool; however, for future versions will be included other primary features OSM classification.

The facilities chosen were divided into two categories, depending of which geometry were thought to display on the map. For example, facilities who have a big dimension on field (Hospitals, Universities, Schools) will be displayed on the map using polygon geometries from OSM. In other hand, facilities which dimension are not too big were displayed as point geometries. The geometric transformations were done in the [ETL script](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/blob/main/ETL/functions.py).

![WhatsApp Image 2023-02-26 at 18 25 37](https://user-images.githubusercontent.com/126191930/221629647-1527a6b5-0e10-4295-9aad-0d8054aa68ae.jpeg)


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



https://user-images.githubusercontent.com/126191930/221422672-94b57a01-3cb4-4c95-b105-d778de6bfeb3.mp4



# API

In the API part some functions were develop to the user get:
- a search connected with the front-end to show the results in a map 
- all information from the database considering a geometry ("/facilities_point" and "/facilities_polygon");
- a specific information in each table using an ID number ("/facilities_point/<id>" and "/facilities_polygon/<id>");

# How can I run Lisbon Search Engine?
    
  If it is necessary, you can create a lisbon_engine environment in Anaconda to run this application, running the code below:

    conda create -n lisbon_engine

    conda activate lisbon_engine

After it, you need to install all the packages necessary for this application running the code below:

    conda install --file requirements.txt --channel conda-forge
     
  
     geopandas
     pandas
     ipykernel
     requests
     osmnx>=1.3
     sqlalchemy<=2.0
     psycopg2
     GeoAlchemy2
     shapely
     numpy
     flask
     Flask-SQLAlchemy
                    
     The version of "sqlalchemy" must be before 2.0, because newer versions have a bug in "to_postgis" function, where the append doesn'n work. 
     
- Creating the database in PgAdmin, the schemas and tables structure of the project you should run the SQL scripts on [database folder](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/tree/main/DB).
- Running the [main.py](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/blob/main/main.py) to download the data, to transform and load to the database.
- Finally, running the [API.py](https://github.com/ProgrammingCourse2023/Lisbon_Search_Engine/blob/main/API.py) to extract the information inside the database and display in the front end.
          
          
 # FRONT END

In the front end has been developed search functions to retrieve the data stored in the database to show the information using pop-ups of each class. The video below shows an example, searching for a type of facility and displaying the information about it in Lisbon.

https://user-images.githubusercontent.com/126191930/221423739-3abeb051-279f-4e75-81b4-09b11908cf68.mp4

          
The user can also search for some facility using the name of the facility, so the Lisbon Search Engine will show all registers that contain this name. The video below shows an example.

https://user-images.githubusercontent.com/126191930/221424269-1a5f7bb5-a63e-43c6-89ab-7abc57a0dde2.mp4

          
The API also has two functions to the user get all the information about facilities stored in the database at the same time. Only need to write, after the localhost, "facilities_polygon", if the facility is stored in the polygon table, or "facilities_point" if the facility is stored in the point table. The video below shows an example of this application.----
          
          
The last API functions are related to get information from the database, but instead of get all information in the same time it will get a single register, considering some id of the register. Only need to write, after the localhost, "facilities_polygon/<id>", if the facility is stored in the polygon table, or "facilities_point/<id>" if the facility is stored in the point table. The video below shows an example of this application.----
# Limitations and next steps
     
# Authors

 Afsaneh Rasoulian Bachelor´s degree in Surveying Engineering
 Gabriel Duarte Bachelos´s degree in Geography
 Mónica Sofía Roncancio Bachelos´s degree in Surveying Engeneering
