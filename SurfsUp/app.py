# Import the dependencies.
import numpy as np

import sqlalchemy 
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with = engine)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)


#################################################
# Flask Setup
#################################################
# Define Flask application

app = Flask(__name__)

#################################################
# Flask Routes
#################################################
#Defining Flask routes

#Home_page route
@app.route("/")

def home_page():
    """List of all available API routes"""
    return(
        "<h1 style='color: #008000'>Welcome to Climate Analysis of Hawaii </h1><br/>"
        "<h2 style='color: #0000FF'>Avialable URLs for the Hawaii Dataset</h2>"
        "<h3 style='color: #6495ED'>List of Precipitation Analysis Results for the last 12 months from the dataset Hawaii (hawaii.sqlite):</h3><br/>"
        f"/api/v1.0/precipitation<br/>"
        "<h3 style='color: #6495ED'>List of Stations from the dataset Hawaii (hawaii.sqlite):</h3><br/>"
        f"/api/v1.0/stations<br/>"
        "<h3 style='color: #6495ED'>Dates and temperature observations of the most active Station for the previous year from the dataset Hawaii (hawaii.sqlite):</h3><br/>"
        f"/api/v1.0/tobs<br/>"
         "<h3 style='color: #6495ED'>List of min/max/avr temps for a specified start_date from the dataset Hawaii (hawaii.sqlite):</h3><br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"<p style='color: #FF0000'> Make sure to follow this format YYYY-MM-DD for specifying the start_date<br/> example url: http://127.0.0.1:5000/api/v1.0/2016-08-23 </p><br/>"
          "<h3 style='color: #6495ED'>List of min/max/avr temps for a specified start-end range from the dataset Hawaii (hawaii.sqlite):</h3><br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;"
        f"<p style='color: #FF0000'> Make sure to follow this format YYYY-MM-DD for specifying the start and end dates<br/> example url: http://127.0.0.1:5000/api/v1.0/2016-08-23/2016-12-23 </p><br/>"
)


#Precipitation route
@app.route("/api/v1.0/precipitation")

def precipitation():

    """Retrieving the last 12 months of precipitation data from the precipitation analysis """

    #create session link to our sqlite database
    session = Session(engine)

    #Query the Measurement table and find the most recent date in it
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    most_recent_date = dt.datetime.strptime(recent_date,'%Y-%m-%d').date()
    
    #Calculate the date one year previous than the most recent date from the Measurement table
    one_year_before_date = most_recent_date - dt.timedelta(days=365)

    #Perform a query to retrieve the data and precipitation scores
    precipitation_score_and_data = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= one_year_before_date).all()

    #convert the query to a dictionary using date as the key and prcp as the value
    precipitation_dict = {}
    for date, prcp in precipitation_score_and_data:
        precipitation_dict[date] = prcp

    #close the session
    session.close()

    #Return the JSON representation of your dictionary.

    return jsonify({"Date and Precipitation for one year prior to the last date in the dataset": precipitation_dict})


# List of stations route from the dataset.
@app.route("/api/v1.0/stations")

def stations():
     
     """Retunr a list of all Stationis"""
     
     #create session link to our sqlite database
     session = Session(engine)

     #Query the station table in the dateset to return a list of stations
     stations_query = session.query(Station.station,Station.name,Station.latitude, Station.longitude,Station.elevation).all()

     #close the session
     session.close()

     #Create station list to return the json list of our stations
     all_stations_list = []

     for station,name,latitude,longitude,elevation in stations_query:
         station_dict = {}
         station_dict['station'] = station
         station_dict['name'] = name
         station_dict['latitude'] = latitude
         station_dict['longitude'] = longitude
         station_dict['elevation'] = elevation

         all_stations_list.append(station_dict)

    #Return the JSON representation of all the stations
     return jsonify({"List of Stations in Hawaii for this dataset":all_stations_list})

#tobs route to get the tempreture observations for the most-active station of previous year within dataset
@app.route("/api/v1.0/tobs")

def tobs():

    """Return a JSON list of temperature observations for the previous year"""
    #create session link to our sqlite database
    session = Session(engine)

    #Query the Measurement table and find the most recent date in it
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

    #convert the string 'recent_date' to the datetime object 'most_recent_date'
    most_recent_date = dt.datetime.strptime(recent_date,'%Y-%m-%d').date()
    
    #Calculate the date one year previous than the most recent date from the Measurement table
    one_year_before_date = most_recent_date - dt.timedelta(days=365)

    #Query the dates and tobs of most active station from the previous year
    most_active_station = session.query(Measurement.station,func.count(Measurement.station)).\
    group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()


    #query the tempreture observation for the most active station in the previous year
    temp_observation = session.query(Measurement.date,Measurement.tobs).\
     filter(Measurement.station == most_active_station[0], Measurement.date >= one_year_before_date).all()
    
  #create a list for the tobs values

    tobs_list = []

    for date, tobs in temp_observation:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        tobs_list.append(tobs_dict)
    #close the db session
    session.close()

    #return the jsonified representation of this query
    return jsonify({"Most Active Station": most_active_station[0],"Tempreture observation for one year back to the last date in dataset": tobs_list})

#Define min temp, max temp,and avg temp for a specified <start date> route
@app.route("/api/v1.0/<start_date>")

def start_date(start_date):

    """ Fetch the temp observation(min,max,avg) for a specified start date till the end date of this Dataset"""

    #create session link to our sqlite database
    session = Session(engine)

    #Query the Measurement table and find the latest and earliest date to make sure the date entered is withing the range.
    latest_date_string = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    earliest_date_string = session.query(Measurement.date).order_by(Measurement.date).first()[0]

    #convert the string date values to the date object
    latest_date_obj = dt.datetime.strptime(latest_date_string,'%Y-%m-%d').date()
    earliest_date_obj = dt.datetime.strptime(earliest_date_string,'%Y-%m-%d').date()
    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()

    #query for the specified start_date

    if earliest_date_obj <= start_date <= latest_date_obj:


        tobs_start_date = (session.query(Measurement.date,func.min(Measurement.tobs),
                                     func.max(Measurement.tobs),
                                     func.avg(Measurement.tobs)
                                     ).filter(Measurement.date >= start_date, Measurement.date <=latest_date_obj).\
                                     group_by(Measurement.date).all())
    
     

    #create the list to store the values of temp obs
        tobs_strdate_list = []
        for date_value,min_temp,max_temp, avg_temp in tobs_start_date:
            tobs_strdate_dict = {}
            tobs_strdate_dict["Date"] = date_value
            tobs_strdate_dict["TMIN"] = min_temp
            tobs_strdate_dict["TMAX"] = max_temp
            tobs_strdate_dict["TAVG"] = avg_temp

            tobs_strdate_list.append(tobs_strdate_dict)
   
     
    #Return the Jsonified response for the tempreture of specified start_date
        return jsonify({"Tempreture observation(TMIN, TMAX,TAVG) from the specified start_date till the end date of the dataset": tobs_strdate_list})
    
    else:
        return jsonify({"error":"The specified start date is not within the date range of this dataset"}),404
    
#close db session
session.close()

#Define min temp, max temp,and avg temp for a specified <start date> and <end_date> route
@app.route("/api/v1.0/<start_date>/<end_date>")

def start_end_date(start_date,end_date):

    """ Fetch the temp observation(min,max,avg) for a specified start_date and end_date"""
    
    #create session link to our sqlite database
    session = Session(engine)

    #Query the Measurement table and find the latest and earliest date to make sure the dates entered is withing the 
    latest_date_string = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    earliest_date_string = session.query(Measurement.date).order_by(Measurement.date).first()[0]

    #convert the string date values to the date object
    latest_date_obj = dt.datetime.strptime(latest_date_string,'%Y-%m-%d').date()
    earliest_date_obj = dt.datetime.strptime(earliest_date_string,'%Y-%m-%d').date()
    start_date = dt.datetime.strptime(start_date,'%Y-%m-%d').date()
    end_date = dt.datetime.strptime(end_date,'%Y-%m-%d').date()

    if (end_date > start_date):

        #Making sure the start and end dates are within the date range of the Measurement table
        if (earliest_date_obj <= start_date <= latest_date_obj) & (earliest_date_obj <= end_date <= latest_date_obj):

            #Query for the tobs within the specified start and end date range
            tobs_start_end_date = (session.query(func.min(Measurement.tobs),
                                    func.max(Measurement.tobs),
                                    func.avg(Measurement.tobs)).filter(Measurement.date >= start_date, Measurement.date <= end_date).\
                                    group_by(Measurement.date).all())
            
            #close db session
            session.close()

            #Create list for this start_end_date query
            tobs_start_end_date_list = []

            for min_temp,max_temp,avg_tem in tobs_start_end_date:
                tobs_start_end_date_dict = {}

                tobs_start_end_date_dict["TMIN"] = min_temp
                tobs_start_end_date_dict["TMAX"] = max_temp
                tobs_start_end_date_dict["TAVG"] = avg_tem

                tobs_start_end_date_list.append(tobs_start_end_date_dict)
            
            #Return JSON representation    
            return jsonify({"Tempreture observation(TMIN, TMAX,TAVG) from the specified start_date till the specified end_date ": tobs_start_end_date_list }) 

        #error if the specified dates are not within the date column range of this dataset    
        else:
            return jsonify({"error":"The specified start and end date is not within the date range of this dataset"}),404

    #error for end_date < start_date
    else:
        return jsonify({"error":"The end_date should be bigger/later than the start_date"})

















