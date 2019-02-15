# data-doggr

"In California, an idle well is a well that has not been used for two years or more and has not yet been properly plugged and abandoned to the Division of Oil, Gas, and Geothermal Resource’s (DOGGR) satisfaction. Plugging and abandonment involves permanently sealing the well with a cement plug to isolate the oil- and gas-bearing geologic formation from water. If a well is not properly plugged and abandoned, it may provide a path for oil, gas, or other contaminants to migrate through the well and into drinking water or to the surface. There are approximately 30,000 wells in California categorized as idle."

"DOGGR has proposed updated regulations to improve maintenance of idle wells. The regulations specify far more rigorous testing requirements that will better protect public safety and the environment from the potential threats posed by idle wells. The regulations will require idle wells be tested and, if necessary, repaired, or plugged and abandoned."

-https://www.conservation.ca.gov/dog/idle_well

"Idle wells are wells which are not in use for production, injection, or other purposes, but also have not been permanently sealed.  DOGGR has changed the definition of idle wells from five years of no productivity to two years of no productivity, in response to legislation.  Approximately 29,000 wells now fall into that category.  Idle wells are the focus of current regulation because wells that are idle for a prolonged period of time can deteriorate if not maintained, and then could become a potential public safety or environmental problem.  Since 1977, California has permanently sealed about 1,400 wells lacking a responsible operator at a cost of $29.5 million, according to DOGGR’s reports."

-https://www.californiaenvironmentallawblog.com/oil-and-gas/doggr-issues-revised-regulations-for-uic-and-idle-wells/


Questions raised:  

    Does 30,000 idle wells seem reasonable based on the State's new definition of an idle well?
    
    Is 30,000 idle wells reasonable for more lenient definitions of inactivity (10 years)?
    
    The State was required to plugged and abandoned 1,400 wells since 1977. Who is to blame?
    
What Data is available:

        The DOGGR website contains a summary documenting each well in California. Assuming that the summary is correct and all wells are accounted for(not a fair assumption). We can make statements on the population size n(103,450 wells).
        
        Each well has a unique API number specific to it. If a well is ACTIVE (not plugged or abandoned), the production history by month (present~1954) is available in a downloadable excel file. 
        

Experimental Designs:

    1) (Over 3 years of inactivity from 2-1-2019 means the well is idle)

    Null Hypothesis: H0 mean = 30000 , p = 30000/103450
    Alt. Hypothesis: HA mean > 30000 ,  p = sample idle wells/sample total
    alpha = .05


    
    2) (Over 10 years of inactivity from 2-1-2019 means the well is idle)
    
    Null Hypothesis: H0 mean = 30000 , p = 30000/103450
    Alt. Hypothesis: HA mean > 30000 , p = sample idle wells/sample total
    alpha = .05
    
Dependencies and Execution:

    ChromeDriver
    python3.6 or higher
    other..
    
    
    1) Clone the repository
        ### If you want to scrape additional well data
        1a) $.. python3.6 doggr_scrape.py #select desired search parameters
            $..  page_scrape() .. to begin downloading production history
            ###production.csv already contains a sample of 2449 wells and their production 
        
        1b) OPTIONAL $.. python3.6 db_parse.py 
            $.. sum_parse()
            $.. parse_excel('PATH/TO/DOWNLOADED/EXCEL/FILES/*.xlsx')
            
    2) $.. python3.6 load_post.py
        2a) $.. pg_load_table('PATH/TO/SUMMARY.CSV',
               'summary', 'databasename', 'host', 'username')
            $.. pg_load_table('PATH/TO/PRODUCTION.CSV',
               'production', 'databasename', 'host', 'username')
    
    3) $.. python3.6 pg.py
    
    
    

    
    





