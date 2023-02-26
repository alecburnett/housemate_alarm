#!/usr/bin/env python3

import subprocess
import pandas as pd
from datetime import datetime
import psycopg2
import os

# replace with the IP address you want to ping
devices = {
    "alex_xiaomi": "192.168.0.2",
    "alex_samsung": "192.168.0.25",
    "alex_work_laptop": "192.168.0.26",
    "georgina_iphone": "192.168.0.5",
    "georgina_mac:": "192.168.0.8"
}

timestamp = datetime.now()

# Create a list to store the ping results and datetime values
results = []

# Loop through the values in the dictionary
for value in devices.values():
    # Ping the IP address
    ping_result = subprocess.run(['ping', '-c', '1', value], stdout=subprocess.PIPE)
    
    # Check the result and append to the results and datetimes lists
    if ping_result.returncode == 0:
        results.append("connected")
    else:
        results.append("offline")

# Create a data frame from the results, datetimes, and devices dictionary
df = pd.DataFrame({"device": list(devices.keys()), "ip_address": list(devices.values()), "status": results, "datetime": timestamp})

import credentials

# Define a function to save the data frame to a PostgreSQL database
def save_to_postgres(df, table_name, dbname, host, port, user, password):
    # Create a connection to the database
    conn = psycopg2.connect(
        dbname=os.environ['dbname'],
        host=os.environ['host'],
        port=os.environ['port'],
        user=os.environ['user'],
        password=os.environ['password']
    )
    
    # Create a cursor to execute SQL commands
    cur = conn.cursor()
    
    # Create the table if it doesn't already exist
    create_table_query = f"CREATE TABLE IF NOT EXISTS device_connection_history (device TEXT, ip_address TEXT, status TEXT, datetime TIMESTAMP)"
    cur.execute(create_table_query)
    
    # Insert the data frame rows into the table
    for _, row in df.iterrows():
        insert_row_query = f"INSERT INTO device_connection_history (device, ip_address, status, datetime) VALUES (%s, %s, %s, %s)"
        cur.execute(insert_row_query, (row["device"], row["ip_address"], row["status"], row["datetime"]))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to save the data frame to the PostgreSQL database
save_to_postgres(df, "ping_results", "my_db", "localhost", 5432, "my_user", "my_password")
print(df)
