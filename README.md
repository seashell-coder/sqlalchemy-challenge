# sqlalchemy-challenge
---------------------------------
Content of this repository
---------------------------------
-SurfUps directory:<br/>
    -climate_starter.jpynb <--> This is the analysis file for the SQLAlchemy part<br/>
    -app.py <--> This is the Flask app, created via python using flask library<br/>
    -Resources directory:<br/>
        -hawaii.sqlite <--> This sqlite db is used in our jupyter notebook and flask app<br/>
        -hawaii_measurement.csv<br/>
        -hawaii_stations.csv

-------------------------------------------------
Instructions for SurfsUp (sqlalchemy-challenge)
-------------------------------------------------
This Challenge is divided in Two Parts: 'Analyze and Explore the Climate Data' & 'Design Your Climate APP'<br/>
**<b> Part 1: Analyze and Explore the Climate Data </b><br/>
    In this section, you’ll use Python and SQLAlchemy to do a basic climate analysis and data exploration of your climate database. Specifically, you’ll use SQLAlchemy ORM queries, Pandas, and Matplotlib.<br/>
    
    --Precipitation Analysis<br/>
        -Find the most recent date in the dataset.<br/>
        -Using that date, get the previous 12 months of precipitation data by querying the previous 12   months of data.<br/>
        -Select only the "date" and "prcp" values.<br/>
        -Load the query results into a Pandas DataFrame. Explicitly set the column names.<br/>
        -Sort the DataFrame values by "date".<br/>
        -Plot the results by using the DataFrame plot method.<br/>

    --Station Analysis<br/>
        -Design a query to calculate the total number of stations in the dataset.<br/>
        -Design a query to find the most-active stations (that is, the stations that have the most rows).<br/>
        -Design a query that calculates the lowest, highest, and average temperatures that filters on the most-active  station id found in the previous query.<br/>
        -Design a query to get the previous 12 months of temperature observation (TOBS) data.<br/>

**<b> Part 2: Design Your Climate App </b><br/>
    You’ll design a Flask API based on the queries that you just developed. To do so, use Flask to create your routes as follows:
        
        1. /
            * Start at the homepage.
            * List all the available routes.

        2. -/api/v1.0/precipitation

            * Convert the query results from your precipitation analysis (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
            * Return the JSON representation of your dictionary.

        3. -/api/v1.0/stations
            * Return a JSON list of stations from the dataset.

        4. -/api/v1.0/tobs
            * Query the dates and temperature observations of the most-active station for the previous year of data.
            * Return a JSON list of temperature observations for the previous year.

        5.  -/api/v1.0/<start> and /api/v1.0/<start>/<end>
            * Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
            * For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
            * For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.

----------------------------------------
References
----------------------------------------
I used a tutorial session assistance with this activity for some of the issue with the diagrams and asked questions for my flask app during office hours.