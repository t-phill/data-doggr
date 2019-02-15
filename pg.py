import psycopg2
import pandas as pd
import sys
from datetime import datetime
import pandas.io.sql as psql
import numpy as np 

try:
    conn = psycopg2.connect(dbname='welldata', user='taylorphillips', host='localhost')
except:
    print("I am unable to connect to the database")
cur = conn.cursor()

try:
    cur.execute('DROP TABLE IF EXISTS pro;')
    cur.execute(
    '''
    CREATE TABLE pro AS
    SELECT api_number, reported_date, days_well_produced, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, well_type, status, pool_code
    FROM production;
    '''
)
except:
    print("Table pro failed")


try:
    cur.execute('DROP TABLE IF EXISTS threepro;')
    cur.execute(
    '''
    CREATE TABLE threepro AS
    SELECT api_number, reported_date, COALESCE(days_well_produced, 0) as days_well_produced, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, well_type, status, pool_code
    FROM pro
    WHERE reported_date > date '2019-02-01' - interval '3 years';
    '''
)
except:
    print("Table threepro failed")

try:
    cur.execute('DROP TABLE IF EXISTS tenpro;')
    cur.execute(
    '''
    CREATE TABLE tenpro AS
    SELECT api_number, reported_date, COALESCE(days_well_produced) as days_well_produced, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, well_type, status, pool_code
    FROM pro
    WHERE reported_date > date '2019-02-01' - interval '10 years';
    '''
)
except:
    print("Table tenpro failed")

cur.execute('DROP TABLE IF EXISTS opsum;')
cur.execute(
    '''
    CREATE TABLE opsum AS
    SELECT threepro.api_number,  summary.operator_name, SUM(threepro.days_well_produced) as days, SUM(threepro.oil_produced_bbl) as oil, SUM(threepro.water_produced_bbl) as water,
    SUM(threepro.gas_produced_mcf) as gas
    FROM threepro
    JOIN summary ON threepro.api_number = summary.api_num
    GROUP BY api_number, operator_name;
    '''
)

cur.execute('DROP TABLE IF EXISTS optensum;')
cur.execute(
    '''
    CREATE TABLE optensum AS
    SELECT tenpro.api_number, summary.operator_name, SUM(tenpro.days_well_produced) as days, SUM(tenpro.oil_produced_bbl) as oil, SUM(tenpro.water_produced_bbl) as water,
    SUM(tenpro.gas_produced_mcf) as gas
    FROM tenpro
    JOIN summary ON tenpro.api_number = summary.api_num
    GROUP BY api_number, operator_name;
    '''
)

op_wells = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) as well_count FROM opsum
GROUP BY operator_name
ORDER BY well_count DESC
''', conn)
op_wells = op_wells.fillna(0)

idle_wells = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) AS idle_count FROM opsum
WHERE days = 0
GROUP BY operator_name
ORDER BY idle_count DESC
''', conn)
idle_wells = idle_wells.fillna(0)

df = op_wells.merge(idle_wells, on='operator_name', how='left').fillna(0)
df['idle_rate'] = df['idle_count']/df['well_count']

samp_n = sum(df['well_count'])
samp_x = sum(df['idle_count'])


op_wells10 = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) as well_count FROM optensum
GROUP BY operator_name
ORDER BY well_count DESC
''', conn)
op_wells10 = op_wells10.fillna(0)

idle_wells10 = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) AS idle_count FROM optensum
WHERE days = 0 
GROUP BY operator_name
ORDER BY idle_count DESC
''', conn)
idle_wells10 = idle_wells10.fillna(0)

df10 = op_wells10.merge(idle_wells10, on='operator_name', how='left').fillna(0)
df10['idle_rate'] = df10['idle_count']/df10['well_count']

samp10_n = sum(df10['well_count'])
samp10_x = sum(df10['idle_count'])

op_sum = psql.read_sql('''
    SELECT threepro.api_number,  summary.operator_name, SUM(threepro.days_well_produced) as days, SUM(threepro.oil_produced_bbl) as oil, SUM(threepro.water_produced_bbl) as water,
    SUM(threepro.gas_produced_mcf) as gas
    FROM threepro
    JOIN summary ON threepro.api_number = summary.api_num
    GROUP BY api_number, operator_name;
    ''', conn)

op10_sum = psql.read_sql('''
    SELECT tenpro.api_number, summary.operator_name, SUM(tenpro.days_well_produced) as days, SUM(tenpro.oil_produced_bbl) as oil, SUM(tenpro.water_produced_bbl) as water,
    SUM(tenpro.gas_produced_mcf) as gas
    FROM tenpro
    JOIN summary ON tenpro.api_number = summary.api_num
    GROUP BY api_number, operator_name;
    ''', conn)

op_sum['idle_arr'] = np.where(op_sum['days']==0, 1, 0)
op10_sum['idle_arr'] = np.where(op10_sum['days']==0, 1, 0)

conn.commit() # <--- makes sure the change is shown in the database
conn.close()
#cur.close()

