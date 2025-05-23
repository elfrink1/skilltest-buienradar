import pandas as pd
import sqlite3


def section_1():
    source = pd.read_json("https://data.buienradar.nl/2.0/feed/json/", orient="records")
    stationmeasurements = pd.DataFrame(source['actual']['stationmeasurements'])

    # Question 1: Create a dataset with the following information about the weather station measurements:
    # measurementid (not in dataset by default), timestamp, temperature, groundtemperature, feeltemperature, windgusts, 
    # windspeedBft, humidity, precipitation, sunpower, stationid

    q1 = stationmeasurements.loc[:, [
	"timestamp",
	"temperature",
	"groundtemperature",
	"feeltemperature",
	"windgusts",
	"windspeedBft",
	"humidity",
	"precipitation",
	"sunpower",
	"stationid"
    ]]
    q1["measurementid"] = q1["stationid"].astype(str) + "_" + q1["timestamp"].astype(str)
    # q1 = q1.set_index("measurementid")

    # Question 2: Create a dataset with the information about the weather stations:
    # stationid, stationname, lat, lon, regio
    q2 = stationmeasurements.loc[:, ["stationid", "stationname", "lat", "lon", "regio"]]
    # q2 = q2.set_index("stationid")

    # Question 3: Store the measurements data and the station data in an SQL database. Use .sqlite for the database. 
    # Consider using index, Primary Key, and defining the relationship between the two tables.
    with sqlite3.connect("buienradar.db") as conn:
        # Create tables only if they do not exist
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stations (
                stationid INTEGER PRIMARY KEY,
                stationname TEXT,
                lat REAL,
                lon REAL,
                regio TEXT
            );
        """)
        
        conn.execute("""
            CREATE TABLE IF NOT EXISTS measurements (
                measurementid TEXT PRIMARY KEY,
                timestamp TEXT,
                temperature REAL,
                groundtemperature REAL,
                feeltemperature REAL,
                windgusts REAL,
                windspeedBft REAL,
                humidity REAL,
                precipitation REAL,
                sunpower REAL,
                stationid INTEGER,
                FOREIGN KEY (stationid) REFERENCES stations(stationid)
            );
        """)
        q1.to_sql("measurements", conn, if_exists="append", index=False)
        q2.to_sql("stations", conn, if_exists="append", index=False)
        

if __name__ == '__main__':
    section_1()
  