#import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect
import datetime as dt
from flask import Flask, jsonify

#Create engine and reflect the database
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

#classes assigned, and other variables created for use in queries
measurement = Base.classes.measurement
station = Base.classes.station

query_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)

#################################################
# Flask Setup
#################################################

#Create an app, being sure to pass __name__
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    
    return (
        f"<h1>Welcome to SQL-Challenge API for climate analysis of Hawaii</h1>"
        f"<h1>Climate App</h1>"
        f"This is a Flask API for Climate Analysis.<br/><br/><br/>"
        f"<h2>Provided are the available routes:</h2>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/>"
        
        f"<h2> I have provided hyperlinked routes to the lists for a better viewing experience. Click the link to see the pages:</h2>"
        f"<ul><li><a href=http://127.0.0.1:5000/api/v1.0/precipitation>"
        f"JSON dictionary of query results from my precipitation analysis of the last 12 months </a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/stations>"
        f"JSON dictionary of weather stations</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/tobs>"
        f"JSON dictionary of the dates and temperature observations of the most-active station for the previous year of data</a></li><br/><br/>"
        f"<li><a href=http://127.0.0.1:5000/api/v1.0/2017-08-23>"
        f"To view results of different date inputs you must change the start and end dates (with YYYY-MM-DD format) in the address bar. You can calculate minimum temperature, the maximum temperature, and the average temperature.</a></li></ul><br/>"
        )
       
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
   
    session.query(measurement.date).\
    filter(measurement.date > query_date).order_by(measurement.date).all()

    sel = [measurement.date, func.avg(measurement.prcp)]

    Yr_query = session.query(*sel).\
    filter(measurement.date > query_date).group_by(measurement.date).order_by(measurement.date).all()
    
    session.close()

    # Convert the query results to a dictionary using date as the key and prcp as the value.
    precip_dict = {}
    for row in Yr_query:
            precip_dict[row.date] = row[1]

    # Return the JSON representation of dictionary.
    return jsonify(precip_dict)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    #q1 queries the station names listed from the station table
    q1 = session.query(station)
    stations = q1.all()

    session.close()

    stations_dict = {}
    for row in stations:
        stations_dict[row.station] = row.name
        
    # Return the JSON representation of dictionary.
    return jsonify(stations_dict)

@app.route("/api/v1.0/tobs")
def activestations():
    session = Session(engine)
    
    #q2 queries the last 12 months of temperature observations from station USC00519281 AKA the most active station.
    q2 = session.query(measurement.date, measurement.tobs).filter(measurement.station == 'USC00519281').\
    filter(measurement.date > query_date).group_by(measurement.date).order_by(measurement.date.desc()).all()
    
    session.close()
    #Convert the query results to a dictionary using date as the key and tobs as the value.
    active_stat_tobs_dict = {}
    for row in q2:
        active_stat_tobs_dict[row.date] = row.tobs
        
    return jsonify(active_stat_tobs_dict)

@app.route("/api/v1.0/<start>")
def start(start):
    session = Session(engine)
    
    #temp_data queries the min, max, and, average temperature from the measurement table.  Then filters dates that are greater than or equal to the start date.
    temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).all()

    session.close()
    
    #The query results are iterated and appended to a results_list 
    results_list = []
    for min_temp, avg_temp, max_temp in temp_data:
        results_list.append(min_temp)
        results_list.append(max_temp)
        results_list.append(avg_temp)

    return jsonify(results_list)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
    session = Session(engine)
    
    #Similar to the start() with the addition of a further query to filter dates that occur on or after the start date and on or before the end date
    temp_data = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
    filter(measurement.date >= start).filter(measurement.date <= end).all()
    
    session.close()
    #The query results are iterated and appended to a results_list
    results_list = []
    for min_temp, avg_temp, max_temp in temp_data:
        results_list.append(min_temp)
        results_list.append(max_temp)
        results_list.append(avg_temp)
        
    return jsonify(results_list)

if __name__ == "__main__":
    app.run(debug=True)
