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
    cur.execute('DROP TABLE IF EXISTS pro;')
    cur.execute(
    '''
    CREATE TABLE pro AS
    SELECT api_number, reported_date, days_well_produced, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, well_type, status, pool_code
    FROM production;
    '''
)
except:
    print("Nope didn't work")

try:
    cur.execute('DROP TABLE IF EXISTS threepro;')
    cur.execute(
    '''
    CREATE TABLE threepro AS
    SELECT api_number, reported_date, days_well_produced, oil_produced_bbl, water_produced_bbl, gas_produced_mcf, well_type, status, pool_code
    FROM production
    WHERE reported_date > date '2019-02-01' - interval '3 years';
    '''
)
except:
    print("Nope didn't work1")

cur.execute('DROP TABLE IF EXISTS opsum;')
cur.execute(
    '''
    CREATE TABLE opsum AS
    SELECT threepro.api_number,  summary.operator_name, SUM(threepro.days_well_produced) as days, SUM(threepro.oil_produced_bbl) as oil, SUM(threepro.water_produced_bbl) as water,
    SUM(threepro.gas_produced_mcf) as gas
    FROM threepro
    JOIN summary ON threepro.api_number = summary.api_num
    GROUP BY api_number, operator_name, well_type;
    '''
)
op_wells = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) as well_count FROM opsum
GROUP BY operator_name
ORDER BY well_count DESC
''', conn)

idle_wells = psql.read_sql('''
SELECT operator_name, COUNT(operator_name) AS idle_count FROM opsum
WHERE days = 0
GROUP BY operator_name
ORDER BY idle_count DESC
''', conn)

# test_wells = psql.read_sql('''
# SELECT operator_name, COUNT(operator_name) as idle FROM opsum
# WHERE days = 0 
# GROUP BY operator_name
# ORDER BY operator_name
#     (SELECT operator_name, COUNT(operator_name) as total FROM opsum)
# ''', conn)




# try:
#     cur.execute('DROP TABLE IF EXISTS opsum;')
#     cur.execute(
#     '''
#     CREATE TABLE opsum AS
#     SELECT api_number, well_type, SUM(oil_produced_bbl) as oil, 
#     SUM(water_produced_bbl) as water, 
#     SUM(gas_produced_mcf) as gas,
#     SUM(days_well_produced) as dval 
#     FROM r
#     GROUP BY api_number, well_type;
# #     '''
# )
# except:
#     print("Nope didn't work1")
# try:
#     cur.execute('DROP TABLE IF EXISTS op;')
#     cur.execute(
#     '''CREATE TABLE op AS
#     SELECT ragg.api_number, summary.operator_name, ragg.well_type, ragg.oil, ragg.water, ragg.gas, ragg.dval
#     FROM ragg
#     JOIN summary
#     ON ragg.api_number = summary.api_num;
#     '''
# )
    # dataframe = psql.read_sql('''SELECT ragg.api_number, summary.operator_name, ragg.well_type, ragg.oil, ragg.water, ragg.gas, ragg.dval
    #                         FROM ragg
    #                         JOIN summary
    #                         ON ragg.api_number = summary."api_#"''', conn)

    

#     #data2 = psql.read_sql('select operator_name, (count(*)/1856) as idle_rate from op where dval = 0 group by operator_name', conn)

# except:
#     print("Nope didn't work2")






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

