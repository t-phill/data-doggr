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
    cur.execute('DROP TABLE IF EXISTS Table;')
    #cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
    cur.execute('''CREATE TABLE test ("API Number" VARCHAR(255),
                                 "Production Date" VARCHAR(255),
                                "Oil Produced (bbl)" VARCHAR(255),
                                "Water Produced (bbl)" VARCHAR (255), 
                                "Gas Produced (Mcf)" VARCHAR(255), 
                                "Days Well Produced" VARCHAR(255), 
                                "Gravity of Oil" VARCHAR(255), 
                                "Casing Pressure" VARCHAR(255), 
                                "Tubing Pressure" VARCHAR(255), BTU VARCHAR(255), 
                                "Method of Operation" VARCHAR(255), 
                                "Water Disposition" VARCHAR(255), 
                                "PWT Status" VARCHAR(255), 
                                "Well Type" VARCHAR(255), 
                                Status VARCHAR(255), 
                                "Pool Code" VARCHAR(255), 
                                "Reported Date" DATE);''')
except:
    print("Nope")

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

