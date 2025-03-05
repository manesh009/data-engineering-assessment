import sqlite3
import csv
from datetime import datetime

# SQLite Database file path
DATABASE_FILE = 'sqlite-files/challenge.db'

# Connect to SQLite database (or any other SQL database)
conn = sqlite3.connect(DATABASE_FILE)
cursor = conn.cursor()


# Function to fetch data from the table and calculate CPO, ROAS
def fetch_and_generate_csv():
    cursor.execute('''
    SELECT channel_name, date, cost, ihc, ihc_revenue FROM channel_reporting
    ''')

    results = cursor.fetchall()

    # Define CSV header
    header = ['Channel Name', 'Date', 'Cost', 'IHC', 'IH Revenue', 'CPO (Cost per Order)', 'ROAS (Return on Ad Spend)']

    # Open CSV file for writing
    with open('channel_reporting_output.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        # Write header
        writer.writerow(header)

        # Process and write each row to the CSV file
        for row in results:
            channel_name, date, cost, ihc, ih_revenue = row

            # Calculate CPO (Cost per Order) and ROAS (Return on Ad Spend)
            cpo = cost / ihc if ihc != 0 else 0
            roas = ih_revenue / cost if cost != 0 else 0

            # Write the row data including calculated CPO and ROAS
            writer.writerow([channel_name, date, cost, ihc, ih_revenue, f"{cpo:.2f}", f"{roas:.2f}"])

    print("CSV file 'channel_reporting_output.csv' generated successfully.")


# Fetch data and generate CSV
fetch_and_generate_csv()

# Close the database connection
conn.close()
