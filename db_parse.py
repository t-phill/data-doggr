import pandas as pd 
import numpy as np 
import os
import glob



#excel_names = glob.glob("/Users/taylorphillips/Downloads/*.xlsx")

excel_names = glob.glob("/Users/taylorphillips/galvanize/capstone/test_files/*.xlsx")

excels = [pd.ExcelFile(name) for name in excel_names]

frames = [x.parse(x.sheet_names[0], header=3) for x in excels]

frames[1:] = [df[1:] for df in frames[1:]]

combined = pd.concat(frames)

combined = combined[pd.notnull(combined['Well Type'])]

#combined.to_excel("c.xlsx", header=True)

combined.to_csv("test.csv", index=False)


# CREATE TABLE production ("API Number" VARCHAR(255), "Production Date" VARCHAR(255), "Oil Produced (bbl)" VARCHAR(255), "Water Produced (bbl)" VARCHAR (255), "Gas Produced (Mcf)" VARCHAR(255), "Days Well Produced" VARCHAR(255), "Gravity of Oil" VARCHAR(255), "Casing Pressure" VARCHAR(255), "Tubing Pressure" VARCHAR(255), BTU VARCHAR(255), "Method of Operation" VARCHAR(255), "Water Disposition" VARCHAR(255), "PWT Status" VARCHAR(255), "Well Type" VARCHAR(255), Status VARCHAR(255), "Pool Code" VARCHAR(255), "Reported Date" DATE);

# COPY production("API Number","Production Date","Oil Produced (bbl)","Water Produced (bbl)","Gas Produced (Mcf)","Days Well Produced","Gravity of Oil","Casing Pressure","Tubing Pressure",BTU, "Method of Operation","Water Disposition","PWT Status","Well Type",Status,"Pool Code","Reported Date") FROM '/Users/taylorphillips/galvanize/capstone/combined.csv' DELIMITER ',' CSV HEADER;


