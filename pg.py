import psycopg2
import pandas as pd
import sys
from datetime import datetime

try:
    conn = psycopg2.connect(dbname='welldata', user='taylorphillips', host='localhost')
except:
    print("I am unable to connect to the database")
cur = conn.cursor()

today = '2019-02-01'

try:
    cur.execute('DROP TABLE IF EXISTS test;')
    cur.execute('''CREATE TABLE test (api_number NUMERIC NOT NULL,
                                 production_date VARCHAR(255),
                                oil_produced_bbl NUMERIC,
                                water_produced_bbl NUMERIC, 
                                gas_produced_mcf NUMERIC, 
                                days_well_produced NUMERIC, 
                                gravity_of_oil NUMERIC, 
                                casing_pressure NUMERIC, 
                                tubing_pressure NUMERIC, 
                                btu NUMERIC, 
                                method_of_operation NUMERIC, 
                                water_disposition NUMERIC, 
                                pwt_status VARCHAR(255), 
                                well_type VARCHAR(255), 
                                status NUMERIC, 
                                pool_code NUMERIC, 
                                reported_date DATE);''')
except:
    print("Nope didn't work")

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
# #cur.close()

def pg_load_table(file_path, table_name, dbname, host, port, user, pwd):
    '''
    This function upload csv to a target table
    '''
    try:
        conn = psycopg2.connect(dbname=dbname, host=host, port=port,\
         user=user, password=pwd)
        print("Connecting to Database")
        cur = conn.cursor()
        f = open(file_path, "r")
        # Truncate the table first
        cur.execute("Truncate {} Cascade;".format(table_name))
        print("Truncated {}".format(table_name))
        # Load table from the file with header
        cur.copy_expert("copy {} from STDIN CSV HEADER QUOTE '\"'".format(table_name), f)
        cur.execute("commit;")
        print("Loaded data into {}".format(table_name))
        conn.close()
        print("DB connection closed.")

    except Exception as e:
        print("Error: {}".format(str(e)))
        sys.exit(1)

# Execution Example
file_path = '/Users/taylorphillips/galvanize/capstone/test.csv'
table_name = 'test'
dbname = 'welldata'
host = 'localhost'
port = ''
user = 'taylorphillips'
pwd = ''
pg_load_table(file_path, table_name, dbname, host, port, user, pwd)

