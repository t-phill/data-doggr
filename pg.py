import psycopg2
import pandas as pd
import sys
from datetime import datetime
import pandas.io.sql as psql

try:
    conn = psycopg2.connect(dbname='welldata', user='taylorphillips', host='localhost')
except:
    print("I am unable to connect to the database")
cur = conn.cursor()

try:
    cur.execute('DROP TABLE IF EXISTS r;')
    cur.execute(
    '''
    CREATE TABLE r AS
    SELECT api_number, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, days_well_produced, reported_date, well_type
    FROM production
    WHERE reported_date > date '2019-02-01' - interval '3 years';
    '''
)
except:
    print("Nope didn't work")

try:
    cur.execute('DROP TABLE IF EXISTS ragg;')
    cur.execute(
    '''
    CREATE TABLE ragg AS
    SELECT api_number, well_type, SUM(oil_produced_bbl) as oil, 
    SUM(water_produced_bbl) as water, 
    SUM(gas_produced_mcf) as gas,
    SUM(days_well_produced) as dval 
    FROM r
    GROUP BY api_number, well_type;
    '''
)
except:
    print("Nope didn't work")
try:
    cur.execute('DROP TABLE IF EXISTS op;')
    cur.execute(
    '''CREATE TABLE op AS
    SELECT ragg.api_number, summary.operator_name, ragg.well_type, ragg.oil, ragg.water, ragg.gas, ragg.dval
    FROM ragg
    JOIN summary
    ON ragg.api_number = summary."api_#";
    '''
)
    dataframe = psql.read_sql('''SELECT ragg.api_number, summary.operator_name, ragg.well_type, ragg.oil, ragg.water, ragg.gas, ragg.dval
                            FROM ragg
                            JOIN summary
                            ON ragg.api_number = summary."api_#"''', conn)

    

    data2 = psql.read_sql('select operator_name, (count(*)/1856) as idle_rate from op where dval = 0 group by operator_name', conn)

except:
    print("Nope didn't work")






#'''select api_number, well_type, sum(oil_produced_bbl) as oil, sum(water_produced_bbl) as water, sum(gas_produced_mcf) as gas from recent group by api_number, well_type;'''
# cur.execute(
#     '''CREATE TABLE fulljoin AS
#     SELECT *
#     FROM test
#     FULL OUTER JOIN summary
#     ON test.api_number = summary."api_#";
#     '''
# )
# #******pd.read_sql********



conn.commit() # <--- makes sure the change is shown in the database
conn.close()
#cur.close()

