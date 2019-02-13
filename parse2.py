import pandas as pd 
import numpy as np 
import os
import glob

excel_names = glob.glob("/Users/taylorphillips/galvanize/capstone/test_files/*.xlsx")

all_data = pd.DataFrame()
for f in excel_names:
    df = pd.read_excel(f)
    all_data = all_data.append(df,ignore_index=True)