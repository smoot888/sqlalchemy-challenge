# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    # Find the most recent date in the data set.
    sel = [measurement.date]
    ordered_dates = session.query(*sel).\
        order_by(desc(measurement.date)).all()
    last_date = ordered_dates[0][0]
    last_date = datetime.strptime(last_date,'%Y-%m-%d').date()
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 

    # Calculate the date one year from the last date in data set.
    new_date = last_date - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,measurement.prcp]
    last_12_months = session.query(*sel).\
        filter(measurement.date > new_date).\
        order_by(measurement.date).all()
    last_12_months

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    dict = pd.DataFrame(last_12_months,columns=['Date','Precipitation'])

    return (jsonify(dict))
    

@app.route("/api/v1.0/stations")
def stations():
    sel = [station.station,func.count(measurement.prcp)]
    stations = session.query(*sel).\
        filter(station.station == measurement.station).\
        group_by(station.station).\
        order_by(desc(func.count(measurement.prcp))).all()
    return (jsonify(stations))
       
@app.route("/api/v1.0/tobs")
def tobs():
    # Design a query to find the most active stations (i.e. which stations have the most rows?)
    # List the stations and their counts in descending order.
    sel = [station.station,func.count(measurement.prcp)]
    stations = session.query(*sel).\
        filter(station.station == measurement.station).\
        group_by(station.station).\
        order_by(desc(func.count(measurement.prcp))).all()
    most_active = stations[0][0]
    # Find the most recent date in the data set for this station.
    sel = [measurement.date]
    ordered_dates = session.query(*sel).\
        filter(measurement.station == most_active).\
        order_by(desc(measurement.date)).all()
    last_date = ordered_dates[0][0]
    last_date = datetime.strptime(last_date,'%Y-%m-%d').date()
    last_date

    # Calculate the date one year from the last date in data set.
    new_date = last_date - timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    sel = [measurement.date,measurement.tobs]
    last_12_months = session.query(*sel).\
        filter(measurement.date > new_date, measurement.station == most_active).\
        order_by(measurement.date).all()
    last_12_months

    # Save the query results as a Pandas DataFrame. Explicitly set the column names
    tobs = pd.DataFrame(last_12_months,columns=['Date','tobs'])
    return (jsonify(tobs))

@app.route("/api/v1.0/<start>")
def start():
    return ()

@app.route("/api/v1.0/<start>/<end>")
def startend():
    return ()