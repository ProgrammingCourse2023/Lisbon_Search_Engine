DROP EXTENSION IF EXISTS postgis;
CREATE EXTENSION postgis;

/*
Creating the tables

*/

DROP TABLE IF EXISTS facilities_polygon;

							
							
CREATE TABLE facilities_polygon (

    id serial PRIMARY KEY,
    name varchar,
    facility varchar,
    phone_number varchar DEFAULT NULL,
    email varchar DEFAULT NULL,
    address varchar,
    osmid bigint,
	element_type varchar,
    website varchar,
    geometry geometry(polygon, 4326)
  
);



DROP TABLE IF EXISTS facilities_point;

							
							
CREATE TABLE facilities_point (

    id serial PRIMARY KEY,
    name varchar,
    facility varchar,
    phone_number varchar DEFAULT NULL,
    email varchar DEFAULT NULL,
    address varchar,
    osmid bigint,
	element_type varchar,
    website varchar,
	opening_hours varchar,
    geometry geometry(point, 4326)
  
);
