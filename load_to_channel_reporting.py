import sqlite3

def fill_channel_reporting_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('sqlite-files/challenge.db')
    cursor = conn.cursor()

    # Define the SQL query to fill the channel_reporting table by querying data from the four tables
    query = '''
        INSERT INTO channel_reporting (channel_name, date, cost, ihc, ihc_revenue)
        SELECT 
            ss.channel_name,                            -- Channel name from session_sources
            ss.event_date,                              -- Event date from session_sources
            IFNULL(SUM(sc.cost), 0),                    -- Total cost from session_costs, default to 0 if NULL
            IFNULL(SUM(acj.ihc), 0),                    -- IHC value from attribution_customer_journey
            IFNULL(SUM(c.revenue), 0)                   -- Total IHC revenue from conversions (assumed as revenue field)
        FROM 
            session_sources ss
        LEFT JOIN 
            session_costs sc ON ss.session_id = sc.session_id        -- Join session_sources with session_costs on session_id
        LEFT JOIN 
            attribution_customer_journey acj ON ss.session_id = acj.session_id  -- Join session_sources with attribution_customer_journey on session_id
        LEFT JOIN 
            conversions c ON ss.user_id = c.user_id            -- Join session_sources with conversions on session_id
        WHERE
            ss.event_date IS NOT NULL                                  -- Ensure that event_date is available in session_sources
        GROUP BY 
            ss.channel_name, ss.event_date;                            -- Group by channel_name and event_date
    '''

    # Execute the query
    cursor.execute(query)

    # Commit the transaction to save the changes
    conn.commit()

    # Close the connection
    conn.close()

    print("Channel reporting table has been successfully updated.")
