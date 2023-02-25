CREATE VIEW public.facilities_polygon_geojson as
SELECT id,
	element_type, 
	osmid,
	facility,
      name,
      address,
      phone_number,
      email,
      website,
	st_asGeoJSON(geometry) as geojson
from public.facilities_polygon; 


CREATE VIEW public.facilities_point_geojson as
SELECT id,
	element_type, 
	osmid,
	facility,
      name,
      address,
      phone_number,
      email,
      website,
      opening_hours,
	st_asGeoJSON(geometry) as geojson
from public.facilities_point; 