import sqlite3


# Function to insert data into the attribution_customer_journey table
def insert_data_to_attribution_customer_journey(conv_id, session_id, ihc):
    # Connect to the SQLite database
    conn = sqlite3.connect('sqlite-files/challenge.db')
    cursor = conn.cursor()

    # SQL query to insert data into the table
    insert_query = '''
    INSERT INTO attribution_customer_journey (conv_id, session_id, ihc)
    VALUES (?, ?, ?)
    '''

    try:
        # Execute the insertion query with the given parameters
        cursor.execute(insert_query, (conv_id, session_id, ihc))

        # Commit the transaction
        conn.commit()

        print("Data has been sucessfully added to attribution customer journey table!")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting data: {e}")

    finally:
        # Close the connection
        conn.close()

