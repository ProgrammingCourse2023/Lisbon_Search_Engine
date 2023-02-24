from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import psycopg2
import json


# import os

DB_CONFIG = {
    "database": "programming_project",
    "username": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5433"}

# Notice, normally this is set with environment variables on the server
# machine do avoid exposing the credentials. Something like


# Create a flask application

app = Flask(__name__)

# Set the database connection URI in the app configuration



username = DB_CONFIG['username']
password = DB_CONFIG['password']
host = DB_CONFIG['host']
port = DB_CONFIG['port']
database = DB_CONFIG['database']
database_uri = f"postgresql://{username}:{password}@{host}:{port}/{database}"

# Create object to control SQLAlchemy from the Flask app

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5433/programming_project'
db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)



# Matches  table 
class facilities_polygon(db.Model):
    __tablename__ = "facilities_polygon_geojson"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    element_type = db.Column(db.Text)
    osmid = db.Column(db.Integer)
    facility = db.Column(db.Text)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    geojson = db.Column(db.Text)
    #geometry = db.Column(Geometry('POLYGON', srid=4326))

     # Because we want to use this object to insert data into the database
    # We need to be able to create an object from the POST request body


class facilities_point(db.Model):
    __tablename__ = "facilities_point_geojson"
    __table_args__ = {"schema": "public"}
    id = db.Column(db.Integer, primary_key=True)
    element_type = db.Column(db.Text)
    osmid = db.Column(db.Integer)
    facility = db.Column(db.Text)
    name = db.Column(db.Text)
    address = db.Column(db.Text)
    phone_number = db.Column(db.Text)
    email = db.Column(db.Text)
    website = db.Column(db.Text)
    opening_hours = db.Column(db.Text)
    geojson = db.Column(db.Text)
    #geometry = db.Column(Geometry('POINT', srid=4326))


conn = psycopg2.connect(dbname= "programming_project",
    user="postgres",
    password= "postgres",
    host= "localhost",
    port= "5433")

@app.get('/search/<keyword>')
def search(keyword):
  query=request.args.get('q')

  cur = conn.cursor()
  cur.execute(f"SELECT * FROM public.facilities_polygon_geojson WHERE facility ILIKE '{keyword}'")

  geo = {
    "name": keyword,
    "type": "FeatureCollection",
    "features": []
  }
  for row in cur.fetchall():
    geo["features"].append({
      "type": "Feature",
      "geometry": json.loads(row[9]),
      "properties": {
        "id": row[0],
        "name": row[4],
        "address": row[5]
      }
    })

  if len(geo["features"]) == 0:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM public.facilities_point_geojson WHERE facility ILIKE '{keyword}'")

    for row in cur.fetchall():
      geo["features"].append({
        "type": "Feature",
        "geometry": json.loads(row[10]),
        "properties": {
          "id": row[0],
          "name": row[4],
          "address": row[5]
        }
      })

  return jsonify(geo)

@app.route('/') 
def index(): 
    return render_template('index.html')

"""
@app.route('/', methods =['GET'])
def map_route():
    session = db.session()
    map_table = db.session.query(facilities_polygon).first()
    geometry_geojson = mapping(to_shape(map_table.geometry))
    return render_template('index.html',geometry_geojson=geometry_geojson)   
"""
@app.route('/facilities_point', methods=['GET'])
def get_facilities_point():
  out_facilities_point = []
  for each_facility_point in db.session.query(facilities_point).all():
    del each_facility_point.__dict__['_sa_instance_state']
    out_facilities_point.append(each_facility_point.__dict__)
  return jsonify(out_facilities_point)

@app.route('/facilities_point/<id>', methods=['GET'])
def get_facilities_id_point(id):
    ind_facility_point = facilities_point.query.get(id)
    del ind_facility_point.__dict__['_sa_instance_state']
    return jsonify(ind_facility_point.__dict__)


@app.route('/facilities_polygon', methods=['GET'])
def get_facilities():
  out_facilities = []
  for each_facility in db.session.query(facilities_polygon).all():
    del each_facility.__dict__['_sa_instance_state']
    out_facilities.append(each_facility.__dict__)
  return jsonify(out_facilities)

@app.route('/facilities_polygon/<id>', methods=['GET'])
def get_facilities_id(id):
    ind_facility = facilities_polygon.query.get(id)
    del ind_facility.__dict__['_sa_instance_state']
    return jsonify(ind_facility.__dict__)
 
if __name__ == '__main__':
    
    app.run(debug=True)
 