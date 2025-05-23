import pandas as pd
import sqlite3


def section_2():
    with sqlite3.connect('buienradar.db') as conn:
        # Section 2
        # Question 5: Which weather station recorded the highest temperature?
        q5 = pd.read_sql('''
        SELECT s.stationname, s.stationid, m.temperature
        FROM stations s
        JOIN (SELECT stationid, temperature FROM measurements) m ON s.stationid = m.stationid
        WHERE m.temperature = (SELECT MAX(temperature) FROM measurements)
        ''', conn)

        # Question 6: What is the average temperature? Note: The average temperature is calculated over all measurements in the database
        q6 = pd.read_sql('SELECT AVG(temperature) FROM measurements', conn)

        # Question 7: What is the station with the biggest difference between feel temperature and the actual temperature?
        q7 = pd.read_sql('''
            SELECT s.stationid, s.stationname, m.tempdiff
            FROM stations s
            JOIN (
                SELECT stationid, ABS(temperature - feeltemperature) AS tempdiff
                FROM measurements
            ) m ON s.stationid = m.stationid
            WHERE m.tempdiff = (
                SELECT MAX(ABS(temperature - feeltemperature)) FROM measurements
            )
        ''', conn)

        # Question 8: Which weather station is located in the North Sea?
        q8 = pd.read_sql('''
        SELECT stationid, stationname, regio
        FROM stations
        WHERE regio = "Noordzee"
        ''', conn)

    return q5, q6, q7, q8
    

if __name__ == '__main__':
    q5, q6, q7, q8 = section_2()
    print(q5, q6, q7, q8)
  