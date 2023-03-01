# 1. import Dependencies

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

measurement = Base.classes.measurement
station = Base.classes.station


# 2. Create an app, being sure to pass __name__
app = Flask(__name__)

@app.route("/")
def home():
    """LIST ALL AVAILABLE ROUTES Work in Progress"""

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Calculate the date one year from the last date in data set.
    session.query(measurement.date).\
    filter(measurement.date > '2016-08-23').order_by(measurement.date).all()

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date, func.avg(measurement.prcp)]

    Yr_query = session.query(*sel).\
    filter(measurement.date > '2016-08-23').group_by(measurement.date).order_by(measurement.date).all()
    
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precip_data = []
    for date, prcp in Yr_query:
        if prcp != None:
            precip_dict = {}
            precip_dict[date] = prcp
            precip_data.append(precip_dict)

    # Return the JSON representation of dictionary.
    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    #List the stations from the dataset
    q1 = session.query(station.station.distinct())
    q1.all()
    
    session.close()
    
    stations=[]
    for names, name in q1:
        station_dict = {}
        station_dict[names] = name
        stations.append(station_dict)
        
    # Return the JSON representation of dictionary.
    return jsonify(stations)   
        
        
    
    

if __name__ == "__main__":
    app.run(debug=True)
