import sqlite3
import pandas as pd
from datetime import datetime

# SQLite Database file path
DATABASE_FILE = 'sqlite-files/challenge.db'


# Function to combine date and time into a datetime object
def to_datetime(date_str, time_str):
    datetime_str = f"{date_str} {time_str}"
    return datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')


# Query to build customer journeys
def get_customer_journeys():
    # Create a connection to SQLite database
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()

    # Query to fetch all conversions
    conversion_query = """ 
        SELECT conv_id, user_id, conv_date, conv_time
        FROM conversions ; 
    """
    conversions = pd.read_sql(conversion_query, conn)

    customer_journeys = {}

    for _, conversion in conversions.iterrows():
        conv_id = conversion['conv_id']
        user_id = conversion['user_id']
        conv_timestamp = to_datetime(conversion['conv_date'], conversion['conv_time'])

        # Query to get all sessions for the user before the conversion timestamp
        session_query = """
            SELECT session_id, event_date, event_time, channel_name, holder_engagement, closer_engagement, impression_interaction
            FROM session_sources
            WHERE user_id = ?
            AND datetime(event_date || ' ' || event_time) < ?;
        """

        # Execute query with parameters
        cursor.execute(session_query, (user_id, conv_timestamp))
        sessions = cursor.fetchall()

        # Store the sessions for the given conv_id (Customer journey)
        customer_journeys[conv_id] = [
            {
                'conversion_id': conv_id,
                'session_id': session[0],
                'timestamp': f"{session[1]} {session[2]}",  # Proper string formatting
                'channel_label': session[3],
                'holder_engagement': session[4],
                'closer_engagement': session[5],
                'impression_interaction': session[6],
                'conversion': 0
            } for session in sessions
        ]

    conn.close()  # Close the SQLite connection
    print('Data extracted from tables conversion and session_sources')
    return customer_journeys


# print the customer journeys for further analysis
"""
customer_journeys = get_customer_journeys()

for conv_id, journey in customer_journeys.items():
    print(f"Conversion ID: {conv_id}")
    for session in journey:
        print(
            f"Session ID: {session['session_id']}, Event Timestamp: {session['timestamp']}, Channel: {session['channel_label']}")
"""